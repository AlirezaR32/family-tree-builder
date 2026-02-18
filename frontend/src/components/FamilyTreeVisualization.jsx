import React, { useEffect, useState, useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  Handle,
  Position,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './FamilyTreeVisualization.css';

const nodeTypes = {
  couple: CoupleNode,
  single: SingleNode,
};

function SingleNode({ data }) {
  return (
    <div className={`custom-node single ${data.gender}`}>
      <Handle type="target" position={Position.Top} />
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
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

function CoupleNode({ data }) {
  const { person1, person2 } = data;
  return (
    <div className="couple-node">
      <Handle type="target" position={Position.Top} />
      <div className="couple-container">
        <div className={`couple-person ${person1.gender}`}>
          <div className="node-icon">
            {person1.gender === 'male' ? '👨' : '👩'}
          </div>
          <div className="node-content">
            <div className="node-name">{person1.name}</div>
            <div className="node-id">{person1.id}</div>
            {person1.birth_year && (
              <div className="node-year">متولد {person1.birth_year}</div>
            )}
          </div>
        </div>
        <div className="couple-divider">💕</div>
        <div className={`couple-person ${person2.gender}`}>
          <div className="node-icon">
            {person2.gender === 'male' ? '👨' : '👩'}
          </div>
          <div className="node-content">
            <div className="node-name">{person2.name}</div>
            <div className="node-id">{person2.id}</div>
            {person2.birth_year && (
              <div className="node-year">متولد {person2.birth_year}</div>
            )}
          </div>
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} />
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

    const newNodes = generateNodes(people);
    const newEdges = generateEdges(people);

    setNodes(newNodes);
    setEdges(newEdges);
  }, [people]);

  const generateNodes = (people) => {
    if (people.length === 0) return [];

    // محاسبه نسل‌ها
    const generations = calculateGenerations(people);
    
    // گروه‌بندی افراد بر اساس نسل
    const generationGroups = {};
    people.forEach(person => {
      const gen = generations[person.id];
      if (!generationGroups[gen]) {
        generationGroups[gen] = [];
      }
      generationGroups[gen].push(person);
    });

    const nodes = [];
    const verticalSpacing = 320;
    const horizontalSpacing = 360;

    // برای هر نسل
    Object.keys(generationGroups)
      .sort((a, b) => a - b)
      .forEach((gen, genIndex) => {
        const personsInGen = generationGroups[gen];
        const processed = new Set();
        const couples = [];

        // شناسایی زوج‌ها
        personsInGen.forEach(person => {
          if (processed.has(person.id)) return;

          if (person.spouse) {
            const spouse = people.find(p => p.id === person.spouse);
            if (spouse && personsInGen.includes(spouse)) {
              couples.push([person, spouse]);
              processed.add(person.id);
              processed.add(spouse.id);
              return;
            }
          }

          // افراد بدون همسر
          couples.push([person]);
          processed.add(person.id);
        });

        // محاسبه موقعیت افقی
        const totalWidth = couples.length * horizontalSpacing;
        let currentX = -totalWidth / 2 + horizontalSpacing / 2;

        couples.forEach((couple, index) => {
          if (couple.length === 2) {
            // نود زوج — شناسه زوج را با مرتب‌سازی ساختاری پایدار بسازید
            const ids = [couple[0].id, couple[1].id].sort();
            const coupleId = `couple-${ids.join('-')}`;
            nodes.push({
              id: coupleId,
              type: 'couple',
              position: {
                x: currentX,
                y: genIndex * verticalSpacing,
              },
              data: {
                person1: couple[0],
                person2: couple[1],
              },
            });
          } else {
            // نود تنهایی
            const person = couple[0];
            nodes.push({
              id: person.id,
              type: 'single',
              position: {
                x: currentX,
                y: genIndex * verticalSpacing,
              },
              data: {
                name: person.name,
                id: person.id,
                gender: person.gender,
                birth_year: person.birth_year,
              },
            });
          }

          currentX += horizontalSpacing;
        });
      });

    return nodes;
  };

  const calculateGenerations = (people) => {
    const generations = {};
    const visited = new Set();

    // پیدا کردن ریشه‌های درخت
    const roots = people.filter(p => !p.parents || p.parents.length === 0);

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
      if (person.children && Array.isArray(person.children)) {
        person.children.forEach(childId => {
          assignGeneration(childId, generation + 1);
        });
      }
    };

    roots.forEach(root => {
      assignGeneration(root.id, 0);
    });

    // افرادی که هنوز نسل مشخص ندارند
    people.forEach(person => {
      if (!generations[person.id]) {
        generations[person.id] = 0;
      }
    });

    return generations;
  };

  const generateEdges = (people) => {
    const edges = [];
    const generationMap = calculateGenerations(people);

    people.forEach(person => {
      // رابطه والد-فرزند
      if (person.children && person.children.length > 0) {
        person.children.forEach(childId => {
          // پیدا کردن نود فرزند (ممکن است جزء یک زوج باشد)
          const childPerson = people.find(p => p.id === childId);
          if (!childPerson) return;

          let sourceId = person.id;
          let targetId = childId;

          // اگر فرد جزء یک زوج باشد، از شناسه زوج استفاده کنید (شناسه‌ها را مرتب‌سازی کن)
          const spouse = people.find(
            p => p.spouse === person.id && 
            generationMap[p.id] === generationMap[person.id]
          );
          if (spouse) {
            const ids = [person.id, spouse.id].sort();
            sourceId = `couple-${ids.join('-')}`;
          }

          // اگر فرزند جزء یک زوج باشد
          const childSpouse = people.find(
            p => p.spouse === childId && 
            generationMap[p.id] === generationMap[childId]
          );
          if (childSpouse) {
            const ids = [childId, childSpouse.id].sort();
            targetId = `couple-${ids.join('-')}`;
          }

          edges.push({
            id: `parent-child-${sourceId}-${targetId}`,
            source: sourceId,
            target: targetId,
            type: 'smoothstep',
            animated: false,
            style: { 
              stroke: '#3b82f6', 
              strokeWidth: 2,
            },
            markerEnd: {
              type: MarkerType.ArrowClosed,
              color: '#3b82f6',
              width: 30,
              height: 30,
            },
          });
        });
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
            <span>💕 همسری</span>
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
            if (node.type === 'couple') {
              return '#9333ea';
            }
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
