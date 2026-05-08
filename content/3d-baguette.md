---
title: "3D Baguette"
toc: false
showreadingtime: false
layout: single
draft: true
---

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  h2::before, h3::before { content: none !important; }

  .baguette-3d-wrap {
    width: 100%;
    aspect-ratio: 16 / 5;
    border-radius: 8px;
    background: var(--color-bg-primary, #fcfcfc);
    overflow: hidden;
    position: relative;
    margin-bottom: 1.5em;
  }
  .baguette-3d-wrap canvas {
    display: block;
    width: 100% !important;
    height: 100% !important;
    cursor: grab;
  }
  .baguette-3d-wrap canvas:active { cursor: grabbing; }
  .baguette-3d-hint {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 11px;
    color: #888;
    opacity: 0;
    pointer-events: none;
    letter-spacing: 0.05em;
    transition: opacity 0.5s;
    font-family: ui-monospace, Menlo, Consolas, monospace;
  }
  .baguette-3d-hint.visible { opacity: 1; }
</style>

<h1>3D Baguette</h1>
<div class="baguette-3d-wrap">
  <canvas id="baguette-canvas"></canvas>
  <div class="baguette-3d-hint" id="baguette-hint">drag | scroll to zoom</div>
</div>

<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>

<script type="module">
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const wrap = document.querySelector('.baguette-3d-wrap');
const canvas = document.getElementById('baguette-canvas');
const hint = document.getElementById('baguette-hint');

const scene = new THREE.Scene();
scene.background = null;

const camera = new THREE.PerspectiveCamera(22, wrap.clientWidth / wrap.clientHeight, 0.01, 50);
camera.position.set(0, 0.04, 0.62);

const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
renderer.setSize(wrap.clientWidth, wrap.clientHeight, false);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setClearColor(0x000000, 0);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.minDistance = 0.35;
controls.maxDistance = 1.2;
controls.target.set(0, 0, 0);
controls.autoRotate = true;
controls.autoRotateSpeed = 45.0;
controls.enablePan = false;

let userInteracted = false;
controls.addEventListener('start', () => {
  userInteracted = true;
  controls.autoRotate = false;
  hint.classList.remove('visible');
});

scene.add(new THREE.AmbientLight(0xffffff, 0.55));
const keyLight = new THREE.DirectionalLight(0xfff0d8, 1.4);
keyLight.position.set(2, 3, 2); scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0xc8d8e8, 0.4);
fillLight.position.set(-2, 1, -1); scene.add(fillLight);

const crustVertex = `
varying vec3 vNormal;
varying vec3 vViewDir;
varying vec3 vObjectPos;
void main() {
  vObjectPos = position;
  vec4 worldPos = modelMatrix * vec4(position, 1.0);
  vNormal = normalize(normalMatrix * normal);
  vViewDir = normalize(cameraPosition - worldPos.xyz);
  gl_Position = projectionMatrix * viewMatrix * worldPos;
}
`;

const crustFragment = `
varying vec3 vNormal;
varying vec3 vViewDir;
varying vec3 vObjectPos;
uniform float uReveal;
uniform vec3 uLightDir;

float hash(vec3 p) {
  p = fract(p * vec3(443.8975, 397.2973, 491.1871));
  p += dot(p, p.yzx + 19.19);
  return fract((p.x + p.y) * p.z);
}
float noise(vec3 p) {
  vec3 i = floor(p);
  vec3 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  return mix(
    mix(mix(hash(i+vec3(0,0,0)), hash(i+vec3(1,0,0)), f.x),
        mix(hash(i+vec3(0,1,0)), hash(i+vec3(1,1,0)), f.x), f.y),
    mix(mix(hash(i+vec3(0,0,1)), hash(i+vec3(1,0,1)), f.x),
        mix(hash(i+vec3(0,1,1)), hash(i+vec3(1,1,1)), f.x), f.y), f.z);
}
float fbm(vec3 p) {
  float v = 0.0; float a = 0.5;
  for (int i = 0; i < 4; i++) { v += a * noise(p); p *= 2.1; a *= 0.5; }
  return v;
}

void main() {
  vec3 p = vObjectPos * 30.0;
  float baseNoise = fbm(p);
  float fineNoise = fbm(p * 4.0);
  vec3 deepCrust = vec3(0.40, 0.20, 0.08);
  vec3 midCrust  = vec3(0.72, 0.44, 0.18);
  vec3 highCrust = vec3(0.92, 0.70, 0.36);
  vec3 flourTint = vec3(0.96, 0.88, 0.66);
  vec3 col = mix(deepCrust, midCrust, smoothstep(0.25, 0.55, baseNoise));
  col = mix(col, highCrust, smoothstep(0.55, 0.78, baseNoise));
  col = mix(col, flourTint, smoothstep(0.85, 0.95, baseNoise + fineNoise * 0.3));
  vec3 n = normalize(vNormal);
  float topness = clamp(n.y * 0.5 + 0.5, 0.0, 1.0);
  col = mix(col * 0.75, col, topness);
  float NdotL = clamp(dot(n, normalize(uLightDir)), 0.0, 1.0);
  float lighting = 0.45 + 0.55 * NdotL;
  float fresnel = pow(1.0 - clamp(dot(n, vViewDir), 0.0, 1.0), 2.5);
  col += fresnel * vec3(0.18, 0.12, 0.06);
  col *= lighting;
  float reveal = clamp(uReveal, 0.0, 1.0);
  float visualReveal = smoothstep(0.0, 0.3, reveal);
  gl_FragColor = vec4(col, visualReveal);
}
`;

const crustMaterial = new THREE.ShaderMaterial({
  vertexShader: crustVertex,
  fragmentShader: crustFragment,
  uniforms: {
    uReveal: { value: 0.0 },
    uLightDir: { value: new THREE.Vector3(2, 3, 2).normalize() }
  },
  transparent: true,
  side: THREE.FrontSide
});

const wireMaterial = new THREE.LineBasicMaterial({
  color: 0x9c6c3c, transparent: true, opacity: 0.0
});

let baguetteSolid = null;
let baguetteWire = null;
const startTime = performance.now();
const REVEAL_DURATION = 2000;
const WIRE_FADE_IN = 600;
const WIRE_FADE_OUT_START = 900;
const WIRE_FADE_OUT_END = 2000;
const TOTAL_ROTATIONS = 2.5;
const SPIN_INITIAL = 45.0;
const SPIN_FINAL = 0.6;
let accumulatedRotations = 0;
let lastFrameTime = performance.now();

const loader = new GLTFLoader();
loader.load(
  '/3d-baguette/baguette.glb',
  (gltf) => {
    let geo = null;
    gltf.scene.traverse(obj => { if (obj.isMesh && !geo) geo = obj.geometry; });
    if (!geo) { console.error('No mesh in glTF'); return; }
    geo.center();
    geo.rotateY(Math.PI * 0.5);
    baguetteSolid = new THREE.Mesh(geo, crustMaterial);
    scene.add(baguetteSolid);
    const wireGeo = new THREE.WireframeGeometry(geo);
    baguetteWire = new THREE.LineSegments(wireGeo, wireMaterial);
    scene.add(baguetteWire);
  },
  undefined,
  (err) => console.error('Failed to load baguette.glb:', err)
);

function animate() {
  requestAnimationFrame(animate);
  const elapsed = performance.now() - startTime;
  if (baguetteSolid && baguetteWire) {
    const reveal = Math.min(elapsed / REVEAL_DURATION, 1.0);
    crustMaterial.uniforms.uReveal.value = reveal * reveal * (3.0 - 2.0 * reveal);
    let wireOpacity = 0;
    if (elapsed < WIRE_FADE_IN) wireOpacity = elapsed / WIRE_FADE_IN;
    else if (elapsed < WIRE_FADE_OUT_START) wireOpacity = 1;
    else if (elapsed < WIRE_FADE_OUT_END)
      wireOpacity = 1 - (elapsed - WIRE_FADE_OUT_START) / (WIRE_FADE_OUT_END - WIRE_FADE_OUT_START);
    wireMaterial.opacity = wireOpacity * 0.6;
  }
  const now = performance.now();
  const dt = (now - lastFrameTime) / 1000;
  lastFrameTime = now;
  if (!userInteracted) {
    const progress = Math.min(accumulatedRotations / TOTAL_ROTATIONS, 1.0);
    const eased = 1.0 - Math.pow(1.0 - progress, 2.2);
    const currentSpeed = SPIN_INITIAL + (SPIN_FINAL - SPIN_INITIAL) * eased;
    controls.autoRotateSpeed = currentSpeed;
    accumulatedRotations += dt * (currentSpeed / 60);
  }
  controls.update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
  camera.aspect = wrap.clientWidth / wrap.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(wrap.clientWidth, wrap.clientHeight, false);
});

setTimeout(() => { if (!userInteracted) hint.classList.add('visible'); }, REVEAL_DURATION);
</script>
