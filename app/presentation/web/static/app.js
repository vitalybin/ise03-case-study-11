const jsonHeaders = { 'Content-Type': 'application/json' };

async function request(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  let data;
  try { data = JSON.parse(text); } catch { data = { raw: text }; }
  if (!response.ok) {
    throw new Error(JSON.stringify(data, null, 2));
  }
  return data;
}

function setOutput(id, data) {
  document.getElementById(id).textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
}

async function move(direction) {
  const step_percent = Number(document.getElementById('stepPercent').value);
  const duration_ms = Number(document.getElementById('durationMs').value);
  setOutput('statusOutput', `Sende Schrittbewegung: ${direction} ...`);
  const data = await request(`/api/move/${direction}`, {
    method: 'POST',
    headers: jsonHeaders,
    body: JSON.stringify({ step_percent, duration_ms })
  });
  setOutput('statusOutput', data);
}

document.querySelectorAll('[data-move]').forEach(btn => {
  btn.addEventListener('click', async () => {
    try { await move(btn.dataset.move); }
    catch (e) { setOutput('statusOutput', e.message); }
  });
});

const steerRange = document.getElementById('steerRange');
const throttleRange = document.getElementById('throttleRange');
steerRange.addEventListener('input', () => document.getElementById('steerValue').textContent = steerRange.value);
throttleRange.addEventListener('input', () => document.getElementById('throttleValue').textContent = throttleRange.value);

document.getElementById('sendSteer').addEventListener('click', async () => {
  try {
    const data = await request('/api/steer', {
      method: 'POST', headers: jsonHeaders, body: JSON.stringify({ value: Number(steerRange.value) })
    });
    setOutput('statusOutput', data);
  } catch (e) { setOutput('statusOutput', e.message); }
});

document.getElementById('sendThrottle').addEventListener('click', async () => {
  try {
    const data = await request('/api/throttle', {
      method: 'POST', headers: jsonHeaders, body: JSON.stringify({ value: Number(throttleRange.value) })
    });
    setOutput('statusOutput', data);
  } catch (e) { setOutput('statusOutput', e.message); }
});

async function stopVehicle() {
  const data = await request('/api/throttle', {
    method: 'POST', headers: jsonHeaders, body: JSON.stringify({ value: 0 })
  });
  throttleRange.value = 0;
  document.getElementById('throttleValue').textContent = '0';
  setOutput('statusOutput', data);
}

document.getElementById('hardStop').addEventListener('click', async () => {
  try { await stopVehicle(); } catch (e) { setOutput('statusOutput', e.message); }
});
document.getElementById('stopBtn').addEventListener('click', async () => {
  try { await stopVehicle(); } catch (e) { setOutput('statusOutput', e.message); }
});

document.getElementById('loadCapabilities').addEventListener('click', async () => {
  try { setOutput('capabilitiesOutput', await request('/api/capabilities')); }
  catch (e) { setOutput('capabilitiesOutput', e.message); }
});

document.getElementById('loadStatus').addEventListener('click', async () => {
  try { setOutput('statusOutput', await request('/api/status')); }
  catch (e) { setOutput('statusOutput', e.message); }
});

document.getElementById('loadLidar').addEventListener('click', async () => {
  try { setOutput('statusOutput', await request('/api/lidar')); }
  catch (e) { setOutput('statusOutput', e.message); }
});

document.getElementById('resetBtn').addEventListener('click', async () => {
  try { setOutput('statusOutput', await request('/api/reset', { method: 'POST' })); }
  catch (e) { setOutput('statusOutput', e.message); }
});

document.getElementById('getObject').addEventListener('click', async () => {
  try {
    const objectId = Number(document.getElementById('objectId').value);
    setOutput('objectOutput', await request(`/api/object/${objectId}`));
  } catch (e) { setOutput('objectOutput', e.message); }
});

document.getElementById('moveObject').addEventListener('click', async () => {
  try {
    const objectId = Number(document.getElementById('objectId').value);
    const x = Number(document.getElementById('objectX').value);
    setOutput('objectOutput', await request('/api/object/move', {
      method: 'POST', headers: jsonHeaders, body: JSON.stringify({ objectId, x })
    }));
  } catch (e) { setOutput('objectOutput', e.message); }
});
