var nodes = new vis.DataSet([
  { id: 0, label: "E", color: "#FF6B6B", font: { size: 16, color: "white" }, shape: "circle" },
  { id: 1, label: "T", color: "#4ECDC4", font: { size: 16, color: "white" }, shape: "circle" },
  { id: 2, label: "F", color: "#45B7D1", font: { size: 16, color: "white" }, shape: "circle" },
  { id: 3, label: "id", color: "#A8E6CF", font: { size: 16, color: "black" }, shape: "box" },
]);

var edges = new vis.DataSet([
  { from: 0, to: 1, arrows: "to", color: { color: "#2B7CE9" }, width: 2 },
  { from: 1, to: 2, arrows: "to", color: { color: "#2B7CE9" }, width: 2 },
  { from: 2, to: 3, arrows: "to", color: { color: "#2B7CE9" }, width: 2 },
]);

var container = document.getElementById("mynetwork");
var data = {
  nodes: nodes,
  edges: edges,
};
var options = {
  layout: {
    hierarchical: {
      direction: 'UD',        // Up-Down (de arriba hacia abajo)
      sortMethod: 'directed', // Ordenamiento dirigido
      levelSeparation: 150,   // Separación entre niveles
      nodeSpacing: 200,       // Espaciado entre nodos
      treeSpacing: 200,       // Espaciado entre árboles
      blockShifting: true,    // Permitir movimiento de bloques
      edgeMinimization: true, // Minimizar cruces de edges
      parentCentralization: true, // Centralizar padres
      shakeTowards: 'leaves'  // Sacudir hacia las hojas
    }
  },
  physics: {
    enabled: false 
  },
  nodes: {
    borderWidth: 2,
    borderWidthSelected: 3,
    chosen: true,
    shadow: {
      enabled: true,
      color: 'rgba(0,0,0,0.2)',
      size: 10,
      x: 3,
      y: 3
    }
  },
  edges: {
    smooth: {
      enabled: true,
      type: 'cubicBezier',
      forceDirection: 'vertical',
      roundness: 0.4
    }
  }
};

// Verificar que vis.js esté disponible
if (typeof vis === 'undefined') {
    document.getElementById('mynetwork').innerHTML = 
        '<div style="padding: 50px; text-align: center; color: red; font-size: 18px;">' +
        '❌ Error: La librería vis.js no se ha cargado correctamente.<br>' +
        '🔧 Verifica tu conexión a internet o descarga vis.js localmente.' +
        '</div>';
} else {
    try {
        var network = new vis.Network(container, data, options);
        console.log("✅ Red generada exitosamente");
    } catch (error) {
        console.error("❌ Error al crear la red:", error);
        document.getElementById('mynetwork').innerHTML = 
            '<div style="padding: 50px; text-align: center; color: red; font-size: 18px;">' +
            '❌ Error al generar la visualización: ' + error.message +
            '</div>';
    }
}