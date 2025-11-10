import React, { useState } from 'react'
import { extractFile, runDiffApi } from './api'

function App(){
  const [fileA,setFileA] = useState<File | null>(null)
  const [fileB,setFileB] = useState<File | null>(null)
  const [jsonA,setJsonA] = useState<any>(null)
  const [jsonB,setJsonB] = useState<any>(null)
  const [diff,setDiff] = useState<any>(null)

  return (
    <div style={{padding:20}}>
      <h2>Doaz Mini Viewer</h2>
      <div style={{display:'flex',gap:20}}>
        <div>
          <h4>Base (A)</h4>
          <input type='file' onChange={e=>setFileA(e.target.files?.[0]||null)} />
          <div style={{marginTop:8}}>
            <button disabled={!fileA} onClick={async ()=>{const r=await extractFile(fileA!); setJsonA(r)}}>Extract A</button>
          </div>
          <pre style={{width:400,height:200,overflow:'auto',background:'#f6f6f6'}}>{jsonA?JSON.stringify(jsonA,null,2):'no json'}</pre>
        </div>
        <div>
          <h4>Revised (B)</h4>
          <input type='file' onChange={e=>setFileB(e.target.files?.[0]||null)} />
          <div style={{marginTop:8}}>
            <button disabled={!fileB} onClick={async ()=>{const r=await extractFile(fileB!); setJsonB(r)}}>Extract B</button>
          </div>
          <pre style={{width:400,height:200,overflow:'auto',background:'#f6f6f6'}}>{jsonB?JSON.stringify(jsonB,null,2):'no json'}</pre>
        </div>
      </div>
      <div style={{marginTop:20}}>
        <button disabled={!jsonA||!jsonB} onClick={async ()=>{const r=await runDiffApi(jsonA,jsonB); setDiff(r)}}>Run Diff</button>
      </div>
      <div style={{marginTop:20}}>
        <h4>Diff</h4>
        <pre style={{width:820,height:300,overflow:'auto',background:'#fff'}}>{diff?JSON.stringify(diff,null,2):'no diff'}</pre>
      </div>
    </div>
  )
}
export default App
