async function post(url,data){
 return fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
 .then(r=>r.json());
}
document.getElementById('analyze').onclick=async()=>{
 let t=JSON.parse(document.getElementById('tasks').value||'[]');
 let s=document.getElementById('strategy').value;
 let r=await post('/api/analyze/?strategy='+s,t);
 document.getElementById('output').innerText=JSON.stringify(r,null,2);
}
document.getElementById('suggest').onclick=async()=>{
 let t=JSON.parse(document.getElementById('tasks').value||'[]');
 let s=document.getElementById('strategy').value;
 let r=await post('/api/suggest/?strategy='+s,t);
 document.getElementById('output').innerText=JSON.stringify(r,null,2);
}
