import React, { useEffect, useState, useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './FamilyTreeVisualization.css';

const nodeTypes = {
  person: PersonNode,
};

function PersonNode({ data }) {
  return (
    <div className={`custom-node ${data.gender}`}>
      <div className="node-icon">
        {data.gender === 'male' ? '👨' : '👩'}
      </div>
      <div className="node-content">
        <div className="node-name">{data.name}</div>
        <div className="node-id">{data.id}</div>
        {data.birth_year && (
          <div className="node-year">متولد {data.birth_year}</div>
        )}
      </div>
    </div>
  );
}

function FamilyTreeVisualization({ people, loading }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    if (people.length === 0) {
      setNodes([]);
      setEdges([]);
      return;
    }

    // ایجاد نودها
    const newNodes = generateNodes(people);
    const newEdges = generateEdges(people);

    setNodes(newNodes);
    setEdges(newEdges);
  }, [people]);

  const generateNodes = (people) => {
    // گروه‌بندی افراد بر اساس نسل (عمق در درخت)
    const generations = calculateGenerations(people);
    const nodesPerGeneration = {};

    // شمارش تعداد افراد در هر نسل
    people.forEach(person => {
      const gen = generations[person.id];
      if (!nodesPerGeneration[gen]) {
        nodesPerGeneration[gen] = [];
      }
      nodesPerGeneration[gen].push(person);
    });

    const nodes = [];
    const verticalSpacing = 200;
    const horizontalSpacing = 250;

    Object.keys(nodesPerGeneration).sort((a, b) => a - b).forEach((gen, genIndex) => {
      const personsInGen = nodesPerGeneration[gen];
      const totalWidth = (personsInGen.length - 1) * horizontalSpacing;
      const startX = -totalWidth / 2;

      personsInGen.forEach((person, index) => {
        nodes.push({
          id: person.id,
          type: 'person',
          position: {
            x: startX + index * horizontalSpacing,
            y: genIndex * verticalSpacing,
          },
          data: {
            name: person.name,
            id: person.id,
            gender: person.gender,
            birth_year: person.birth_year,
          },
        });
      });
    });

    return nodes;
  };

  const calculateGenerations = (people) => {
    const generations = {};
    const visited = new Set();

    // پیدا کردن ریشه‌های درخت (افرادی که والد ندارند)
    const roots = people.filter(p => !p.parents || p.parents.length === 0);

    // اگر ریشه‌ای نبود، اولین فرد را به عنوان ریشه در نظر بگیر
    if (roots.length === 0 && people.length > 0) {
      roots.push(people[0]);
    }

    const assignGeneration = (personId, generation) => {
      if (visited.has(personId)) return;
      visited.add(personId);

      generations[personId] = generation;

      const person = people.find(p => p.id === personId);
      if (!person) return;

      // فرزندان
      if (person.children) {
        person.children.forEach(childId => {
          assignGeneration(childId, generation + 1);
        });
      }
    };

    roots.forEach(root => {
      assignGeneration(root.id, 0);
    });

    // افرادی که هنوز نسلشان مشخص نشده
    people.forEach(person => {
      if (!generations[person.id]) {
        generations[person.id] = 0;
      }
    });

    return generations;
  };

  const generateEdges = (people) => {
    const edges = [];

    people.forEach(person => {
      // رابطه والد-فرزند
      if (person.children && person.children.length > 0) {
        person.children.forEach(childId => {
          edges.push({
            id: `${person.id}-${childId}`,
            source: person.id,
            target: childId,
            type: 'smoothstep',
            animated: false,
            style: { stroke: '#4a90e2', strokeWidth: 2 },
            markerEnd: {
              type: MarkerType.ArrowClosed,
              color: '#4a90e2',
            },
            label: 'فرزند',
            labelStyle: { fill: '#4a90e2', fontWeight: 500 },
            labelBgStyle: { fill: '#fff' },
          });
        });
      }

      // رابطه همسری
      if (person.spouse) {
        // فقط یک طرف رابطه را نمایش بده تا خط تکراری نداشته باشیم
        if (person.id < person.spouse) {
          edges.push({
            id: `spouse-${person.id}-${person.spouse}`,
            source: person.id,
            target: person.spouse,
            type: 'straight',
            animated: true,
            style: { stroke: '#e74c3c', strokeWidth: 3, strokeDasharray: '5,5' },
            label: '💕',
            labelStyle: { fill: '#e74c3c', fontSize: 20 },
            labelBgStyle: { fill: '#fff' },
          });
        }
      }
    });

    return edges;
  };

  if (loading) {
    return (
      <div className="tree-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>در حال بارگذاری...</p>
        </div>
      </div>
    );
  }

  if (people.length === 0) {
    return (
      <div className="tree-container">
        <div className="empty-state">
          <div className="empty-icon">🌳</div>
          <h3>درخت خالی است</h3>
          <p>برای شروع، افراد و روابط خانوادگی را اضافه کنید</p>
          <p className="hint">💡 یا از دکمه "بارگذاری داده نمونه" استفاده کنید</p>
        </div>
      </div>
    );
  }

  return (
    <div className="tree-container">
      <div className="tree-header">
        <h3>🌳 نمودار شجره‌نامه</h3>
        <div className="legend">
          <div className="legend-item">
            <div className="legend-line parent-child"></div>
            <span>رابطه والد-فرزند</span>
          </div>
          <div className="legend-item">
            <div className="legend-line spouse"></div>
            <span>رابطه همسری</span>
          </div>
        </div>
      </div>
      
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.1}
        maxZoom={2}
        defaultViewport={{ x: 0, y: 0, zoom: 0.8 }}
      >
        <Background color="#aaa" gap={16} />
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            return node.data.gender === 'male' ? '#4a90e2' : '#e74c3c';
          }}
          nodeStrokeWidth={3}
          zoomable
          pannable
        />
      </ReactFlow>
    </div>
  );
}

export default FamilyTreeVisualization;
