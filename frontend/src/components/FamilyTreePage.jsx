import React, { useEffect, useState } from 'react';
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
import './FamilyTreePage.css';

const nodeTypes = {
  person: PersonNode,
};

function PersonNode({ data }) {
  return (
    <div className={`custom-node ${data.gender}`}>
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

function FamilyTreePage({ people, loading }) {
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
  }, [people, setNodes, setEdges]);

  const generateNodes = (people) => {
    if (people.length === 0) return [];

    const generations = calculateGenerations(people);
    const generationGroups = {};

    people.forEach(person => {
      const gen = generations[person.id];
      if (!generationGroups[gen]) {
        generationGroups[gen] = [];
      }
      generationGroups[gen].push(person);
    });

    const nodes = [];
    const verticalSpacing = 220;
    const horizontalSpacing = 200;
    const spouseSpacing = 120;

    Object.keys(generationGroups)
      .sort((a, b) => a - b)
      .forEach((gen, genIndex) => {
        const personsInGen = generationGroups[gen];
        const processed = new Set();
        const row = [];

        personsInGen.forEach(person => {
          if (processed.has(person.id)) return;

          if (person.spouse) {
            const spouse = people.find(p => p.id === person.spouse);
            if (spouse && generationGroups[gen].includes(spouse)) {
              row.push([person, spouse]);
              processed.add(person.id);
              processed.add(spouse.id);
              return;
            }
          }

          row.push([person]);
          processed.add(person.id);
        });

        const totalWidth = row.reduce((sum, group) => {
          return sum + (group.length === 2 ? spouseSpacing : 0) + horizontalSpacing;
        }, -horizontalSpacing);

        let currentX = -totalWidth / 2;

        row.forEach(group => {
          if (group.length === 2) {
            const [person1, person2] = group;

            nodes.push({
              id: person1.id,
              type: 'person',
              position: {
                x: currentX,
                y: genIndex * verticalSpacing,
              },
              data: {
                name: person1.name,
                id: person1.id,
                gender: person1.gender,
                birth_year: person1.birth_year,
              },
            });

            nodes.push({
              id: person2.id,
              type: 'person',
              position: {
                x: currentX + spouseSpacing,
                y: genIndex * verticalSpacing,
              },
              data: {
                name: person2.name,
                id: person2.id,
                gender: person2.gender,
                birth_year: person2.birth_year,
              },
            });

            currentX += spouseSpacing + horizontalSpacing;
          } else {
            const person = group[0];

            nodes.push({
              id: person.id,
              type: 'person',
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

            currentX += horizontalSpacing;
          }
        });
      });

    return nodes;
  };

  const calculateGenerations = (people) => {
    const generations = {};
    const visited = new Set();

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

      if (person.children) {
        person.children.forEach(childId => {
          assignGeneration(childId, generation + 1);
        });
      }
    };

    roots.forEach(root => {
      assignGeneration(root.id, 0);
    });

    people.forEach(person => {
      if (!generations[person.id]) {
        generations[person.id] = 0;
      }
    });

    return generations;
  };

  const generateEdges = (people) => {
    const edges = [];
    const processedSpouses = new Set();

    people.forEach(person => {
      // رابطه والد-فرزند
      if (person.children && person.children.length > 0) {
        person.children.forEach(childId => {
          edges.push({
            id: `parent-child-${person.id}-${childId}`,
            source: person.id,
            target: childId,
            type: 'smoothstep',
            animated: false,
            style: {
              stroke: '#3b82f6',
              strokeWidth: 3,
            },
            markerEnd: {
              type: MarkerType.ArrowClosed,
              color: '#3b82f6',
              width: 30,
              height: 30,
            },
            data: {
              type: 'parent-child',
            },
          });
        });
      }

      // رابطه همسری
      if (person.spouse && !processedSpouses.has(`${person.id}-${person.spouse}`)) {
        processedSpouses.add(`${person.id}-${person.spouse}`);
        processedSpouses.add(`${person.spouse}-${person.id}`);

        edges.push({
          id: `spouse-${person.id}-${person.spouse}`,
          source: person.id,
          target: person.spouse,
          type: 'smoothstep',
          animated: true,
          style: {
            stroke: '#ef4444',
            strokeWidth: 3,
            strokeDasharray: '8 4',
          },
          label: '💕',
          labelStyle: {
            fill: '#ef4444',
            fontSize: 18,
            fontWeight: 'bold',
          },
          labelBgStyle: {
            fill: 'white',
            fillOpacity: 0.9,
          },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color: '#ef4444',
            width: 25,
            height: 25,
          },
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
            <div className="legend-line spouse"></div>
            <span>رابطه همسری</span>
          </div>
          <div className="legend-item">
            <span style={{ color: '#3498db' }}>🔵 مرد</span>
          </div>
          <div className="legend-item">
            <span style={{ color: '#e91e63' }}>🔴 زن</span>
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

export default FamilyTreePage;
