const BACKEND = (window as any).__BACKEND_URL__ || 'http://localhost:8000'

export async function extractFile(f: File): Promise<any> {
  const fd = new FormData()
  fd.append('file', f)
  const res = await fetch(`${BACKEND}/extract`, { method: 'POST', body: fd })
  return res.json()
}

export async function runDiffApi(a: any, b: any): Promise<any> {
  const res = await fetch(`${BACKEND}/diff`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ base_json: a, revised_json: b })
  })
  return res.json()
}

