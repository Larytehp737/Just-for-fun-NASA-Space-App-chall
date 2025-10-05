import React from 'react'
export default function App(){
  return (
    <div id="app">
      <div className="sidebar">
        <h1>Embiggen Your Eyes</h1>
        <p className="badge">MVP</p>
        <section><h3>Layers</h3>
          <ul>
            <li><label><input type="checkbox" defaultChecked id="chk-heat"/> Heatmap</label></li>
            <li><label><input type="checkbox" defaultChecked id="chk-ann"/> Annotations</label></li>
          </ul>
        </section>
        <section><h3>Export</h3>
          <button id="btn-export">Exporter JSON</button>
        </section>
      </div>
      <div className="viewer"><div id="osd"/></div>
    </div>
  )
}
