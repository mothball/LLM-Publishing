"""Monograph content definitions. Reconstructed from conversation fragments."""

MONOGRAPHS = [

# ============================================================
# 01 — Vectorized Python (most recent)
# ============================================================
{
"num": 1,
"slug": "01-performant-vectorized-python",
"date": "2026-05-17",
"format": "Markdown",
"length": "Parts I–IX",
"pdf": "01-performant-vectorized-python.pdf",
"pdf_available": False,
"title": "Performant Vectorized Python",
"subtitle": "A Technical Monograph on Writing Code That Saturates the Hardware",
"blurb": "From the memory hierarchy and SIMD lanes up through NumPy 2.x dispatch, free-threading, NEP 54, tile DSLs, and a cross-language reality check.",
"abstract_text": "A practitioner-level monograph on writing performant vectorized Python — memory model, NumPy internals, SIMD dispatch, parallelism, GPU paths, and what the maximum looks like across languages.",
"abstract": """
<p>Targeting CPython 3.13/3.14 and NumPy 2.x. Written for practitioners who already
know Python and NumPy and want to understand the machine underneath. The thesis,
threaded through every part: <em>performance work is memory work</em>. A double-precision
multiply costs a few cycles; a fetch from main memory costs two to three hundred.
Vectorized code is fast for two reasons that have different failure modes — it
moves work out of the CPython interpreter, and it gives the compiler something
the SIMD units can chew through. Treat those separately and the gap between
typical numerical code and the hardware roofline collapses.</p>
""",
"toc": [
    "Part I — The Machine (caches, vector units, the Roofline model)",
    "Part II — NumPy Internals (<code>ndarray</code> memory, views vs copies, ufunc execution, broadcasting cost)",
    "Part III — Writing Vectorized Code (<code>ArrayLike</code> + <code>asarray</code>, eliminating temporaries, AoS vs SoA, axis discipline)",
    "Part IV — Reaching Hardware Performance (NumPy 2.x SIMD dispatch, cache blocking, Numba, dtype as a lever)",
    "Part V — Parallelism (the GIL, free-threaded Python 3.13/3.14, the threading decision tree)",
    "Part VI — Measurement (timeit → flame graphs, Roofline analysis, hardware counters)",
    "Part VII — Beyond the CPU (GPU and accelerator paths; Mojo and the compiled-Python frontier)",
    "Part VIII — The Frontier (NEP 54 + Google Highway, language changes, the convergence thesis)",
    "Part IX — Cross-Language Perspective (Python vs C/C++/Java/Julia; a JAX field guide)",
    "Annotated Bibliography (Drepper, Hennessy &amp; Patterson, Roofline, Agner Fog, Rougier, NumPy NEP 38/54, Gorelick &amp; Ozsvald)",
],
"sections": [
{"heading": "The mental model: vectorization is really about memory",
"body": """
<p>The instinct most people carry into performance work is wrong, or at least
incomplete: they think performance means <em>doing fewer operations</em>. On modern
hardware, the dominant cost of numerical code is almost never arithmetic. It is
moving data. The arithmetic units sit idle, starved, waiting for operands.</p>

<p>This reframes everything. "Vectorized" code is fast for two distinct reasons,
and they are worth separating because they have different failure modes:</p>

<ol>
<li><strong>It moves work out of the CPython interpreter.</strong> Each Python bytecode
operation carries enormous overhead: boxed objects, reference counting,
dynamic dispatch, type checks. A Python-level loop over a million floats
pays that tax a million times; a NumPy call pays it once and then runs a
tight C loop.</li>
<li><strong>It gives the compiler something the SIMD units can chew through.</strong>
Contiguous arrays in well-known dtypes are exactly what NumPy's inner
loops — and now its runtime SIMD dispatch via NEP 38/54 — are tuned for.</li>
</ol>
"""},
{"heading": "API boundaries and dtype discipline",
"body": """
<p>Accepting <code>ArrayLike</code> at the API boundary and normalizing internally is
the right pattern:</p>

<pre><code>from numpy.typing import ArrayLike, NDArray
import numpy as np

def propagate(state: ArrayLike, dt: ArrayLike) -> NDArray[np.float64]:
    state = np.asarray(state, dtype=np.float64)
    dt    = np.asarray(dt,    dtype=np.float64)
    ...</code></pre>

<p>Use <code>np.asarray</code>, not <code>np.array</code> — <code>asarray</code> is a no-op when the input is
already a contiguous array of the right dtype, so you avoid a spurious copy.
Pinning <code>dtype</code> explicitly at the boundary prevents silent upcasts to
<code>float64</code> from an unexpected <code>float32</code> input, or object-dtype disasters
from a list of Python ints.</p>
"""},
{"heading": "Layout: AoS vs SoA and the contiguous axis",
"body": """
<p>Memory layout dominates cache behavior. Structure-of-arrays wins for vectorized
math because each operation streams contiguous memory. For a batch of state
vectors, store <code>(6, N)</code> or <code>(N, 6)</code> deliberately. If your hot loop operates
component-wise across the batch, you want each component contiguous:
<code>positions[0]</code> should be a stride-1 view. Generally <code>(6, N)</code> with C-order
gives you that; <code>(N, 6)</code> forces strided access on per-component ops.</p>

<p>Operate along the last axis. NumPy reduction and ufunc inner loops are
fastest when the contiguous axis is the one being iterated.</p>
"""},
{"heading": "Part VIII — the frontier",
"body": """
<p><strong>NEP 54</strong> has progressed beyond draft. NumPy has begun using Google Highway
internally and the roadmap states usage will expand, with SVE work ongoing. The
crucial point for the user: it's internal re-plumbing with <em>no Python or C API
changes</em>. You don't act on it; it silently widens free SIMD coverage —
especially on ARM and future RISC-V. One practical wrinkle: Highway's pragma use
is poorly supported by MSVC, so building NumPy from source on Windows with
full SIMD may need <code>clang-cl</code>.</p>

<p><strong>cuTile</strong> is genuinely new (December 2025, CUDA 13.1). Built on Numba plus a
new compiler stack, draws on Triton, and introduces Tile IR as a virtual ISA.
Worth prototyping to learn the model; Triton is the safer production pick today.</p>

<p>The §31 thesis: at the single-kernel level there is no meaningful performance
ceiling separating compiled-Python tools from C. A well-shaped Numba/JAX/Cython
kernel reaches the same hardware roofline as hand-written <code>-O3 -march=native</code>
C. The cross-language benchmark literature backs this — Julia and C++ broadly
comparable, small wins trading by scenario. The gap between typical numerical
code and the maximum is almost never the language; it's the five fixable things:
unfused temporaries, wrong layout, strided access, oversized dtype, un-exploited
parallelism.</p>
"""},
],
"closing": """
<p>Produced in conversation
<a href="https://claude.ai/chat/71b47249-5fe6-473c-ae99-7ea329bfe075">71b47249</a>
on 2026-05-17. The original markdown lives at
<code>/mnt/user-data/outputs/performant-vectorized-python.md</code> in that
container. Parts VIII–IX were the most time-sensitive — NEP statuses, version
numbers, and tile DSLs will move; Parts I–IV are durable physics.</p>
""",
},

# ============================================================
# 02 — Differentiable GPU-Native Astrodynamics Substrate
# ============================================================
{
"num": 2,
"slug": "02-differentiable-astrodynamics-substrate",
"date": "2026-05-08",
"format": "LaTeX → PDF",
"length": "Technical case",
"pdf": "02-differentiable-astrodynamics-substrate.pdf",
"pdf_available": False,
"title": "A Differentiable, GPU-Native Astrodynamics Substrate",
"subtitle": "A Technical Case for Operational and Strategic Investment",
"blurb": "The SPEPH ceiling, end-to-end differentiability as a deep-learning analogy, and the architectural shift it enables for SDA and fleet management.",
"abstract_text": "Operational SDA rests on propagators whose architecture was locked in two decades ago. End-to-end differentiability and GPU-native batching break the ceiling.",
"abstract": """
<p>Operational space domain awareness (SDA) and satellite fleet management both
rest on numerical orbit propagators whose architectural choices were locked in
two decades ago: hand-derived analytic partial derivatives, CPU-bound integration,
and force-model cards configured per-run with no gradient information available
downstream. The U.S. Space Force's Special Perturbations Ephemeris (SPEPH)
propagator is the operational reference and an excellent example of this
architecture; it is also a structural ceiling on what every downstream tool
built on top of it can do.</p>

<p>This monograph proposes — and makes the operational and strategic case for —
a differentiable, GPU-native astrodynamics substrate that replaces hand-derived
partials with automatic differentiation, replaces single-trajectory CPU integration
with batched GPU propagation, and makes the entire stack (propagator, conjunction
calculator, scheduler) end-to-end differentiable from action to consequence.</p>
""",
"sections": [
{"heading": "Why the current architecture is a ceiling",
"body": """
<p>SPEPH is described in current open documentation as a variable-step Runge-Kutta
of the RK 7(8)/RK 8(9) Fehlberg-Dormand-Prince family with high-fidelity force
models (EGM-96, IAU-1976/1980 precession-nutation, JPL DE430 third-body,
Jacchia-Roberts drag, spherical SRP). The legacy AFSPC code used Gauss-Jackson
8th-order predictor-corrector with an RK starter.</p>

<p>None of that is wrong. What it is, is closed. STMs and partials are hand-derived
per force model; the propagator is a black box to anything downstream that wants
a gradient with respect to a maneuver, a sensor cue, or a schedule decision.
"What ΔV minimizes fuel and preserves the schedule and keeps Pc below threshold"
becomes grid search — running the chain forward many times with different
candidates — with all of grid search's limitations.</p>
"""},
{"heading": "The deep-learning analogy",
"body": """
<p>End-to-end differentiability is why deep learning works. A modern neural network
is a stack of layers — convolutions, attention, normalizations, classification
heads — and the entire stack is differentiable. That is the only reason
gradient descent can train it. If any layer were a black box, training would
be impossible and the field would not exist.</p>

<p>The proposal, in one sentence: <em>bring the same architectural property to the
operational SDA and fleet-management stack.</em> The propagator becomes the bottom
layer of a learning system; the consequences (schedule revenue, fuel consumption,
conjunction probability, customer SLA) become the loss function; the actions
(maneuver ΔV's, tasking schedules, sensor cues) become the parameters. The
gradient-based optimization that trains transformers becomes the gradient-based
optimization that plans maneuvers.</p>
"""},
{"heading": "What end-to-end differentiability enables",
"body": """
<p>Three concrete capabilities require the chain to be unbroken end-to-end, not
just locally differentiable in pieces:</p>
<ul>
<li><strong>Joint optimization across stack layers.</strong> Computing
$\\partial\\text{revenue}/\\partial \\Delta V$ requires the gradient to flow
from the scheduler, through the propagator, through the dynamics, back to the
maneuver decision. Any broken link forces the optimization to decompose into
separately-optimized pieces and the joint optimum is provably unattainable.</li>
<li><strong>Adjoint data assimilation.</strong> Whole-trajectory sensitivity
without finite differences.</li>
<li><strong>Taylor map diffusion for conjunction Pc.</strong> Three orders of
magnitude faster than Monte Carlo on the same ground truth, with gradients
included.</li>
</ul>
"""},
{"heading": "Demo recommendation",
"body": """
<p>Pick one feature and benchmark it against operational tooling, end-to-end, on a
real or representative case. The two highest-impact candidates:</p>
<ul>
<li><strong>(a)</strong> The GA-vs-AD-gradient comparison on a realistic RPO trajectory
design — same RHS, same hardware, wall-clock and convergence curves side by
side. Most viscerally compelling for a technical audience; the speedup is
huge and the comparison is direct.</li>
<li><strong>(b)</strong> Taylor Map Diffusion vs. Monte Carlo Pc on a conjunction case
from your CDM archive. Same MC ground truth, three orders of magnitude
speedup, gradients for free. Most operationally compelling because it
touches conjunction analysis directly.</li>
</ul>
<p>The feature list is what you put in the deck. The benchmark is what closes the room.</p>
"""},
],
"closing": """
<p>Compiled from conversation
<a href="https://claude.ai/chat/2308b2c5-71af-4699-b330-b1624b01eef5">2308b2c5</a>
on 2026-05-08, alongside the JAX and Mojo roadmap monographs (Nos. 03 and 04).
Originally requested as: <em>"Summarize this entire conversation as a LaTeX
monograph that is self-contained, technical and thorough. Render it as a PDF."</em></p>
""",
},

# ============================================================
# 03 — JAX Roadmap
# ============================================================
{
"num": 3,
"slug": "03-jax-astrodynamics-roadmap",
"date": "2026-05-08",
"format": "LaTeX → PDF",
"length": "~21 pages",
"pdf": "03-jax-astrodynamics-roadmap.pdf",
"pdf_available": False,
"title": "A JAX-Native Differentiable, GPU-Native Astrodynamics Substrate",
"subtitle": "Layered Implementation Roadmap from Primitives to Operational Propagator",
"blurb": "Ten layers, each a self-contained deliverable with acceptance criteria, validation, and off-ramps. The composable-existing-components shape.",
"abstract_text": "A JAX-stack implementation roadmap. Ten layers, each a coherent deliverable with explicit acceptance criteria.",
"abstract": """
<p>This monograph specifies a complete implementation roadmap for a high-fidelity
differentiable orbit propagator built on the JAX scientific computing stack,
structured as a layered architecture from the lowest computational primitives
upward to a production-grade propagator with full force-model fidelity,
end-to-end automatic differentiation, GPU-batched parallelism, and operational
interoperability.</p>

<p>Each layer is treated as a self-contained engineering deliverable with explicit
acceptance criteria, validation procedures, dependencies on lower layers, and
potential off-ramps. The intended audience is the technical team that would
actually implement this work; the document serves both as a planning artifact
for resource allocation and as a reference architecture for the implementation
phase. The structure mirrors an analogous Mojo-based roadmap (No. 04) for
direct comparison; identical sections in the two documents address the same
engineering problem in their respective stacks.</p>
""",
"sections": [
{"heading": "Architectural premise",
"body": """
<p>The substrate is structured as ten layers, each a coherent engineering
deliverable with its own acceptance criteria. Below each section heading the
roadmap states (1) what is built, (2) what it depends on from below, (3) what
exists in the JAX ecosystem that can be borrowed, (4) where the engineering
risk concentrates, and (5) the off-ramp if the layer cannot be made to work as
specified.</p>

<p>The structural advantage of the JAX stack is that several layers — automatic
differentiation, batched compilation via <code>vmap</code> and <code>jit</code>, ODE
integration via Diffrax, the optimizer ecosystem in Optax — exist in
production-grade form on day one. The shape of the project is "compose
existing components with carefully-specified glue," not "build the
foundations."</p>
"""},
{"heading": "What's borrowed from the ecosystem",
"body": """
<ul>
<li><strong>JAX core</strong> — tracing, JIT, autograd primitives.</li>
<li><strong>Diffrax</strong> — adaptive RK methods, implicit solvers, dense output,
event detection.</li>
<li><strong>Optax</strong> — gradient-based optimizers for downstream tasking and
maneuver-planning loops.</li>
<li><strong>jaxsgp4</strong> — reference batched SGP4 for parity checks against
operational TLE-driven tooling.</li>
<li><strong>brandeis-orbit / heyoka.py</strong> — reference high-fidelity propagators
to anchor against during validation.</li>
</ul>
"""},
{"heading": "Risk concentrations",
"body": """
<p>The roadmap calls out three layers where JAX-specific friction is unavoidable:</p>
<ol>
<li><strong>Adaptive stepping under tracing.</strong> Diffrax already
solves most of this, but custom solvers (e.g., a Gauss-Jackson port) re-open
the design tension.</li>
<li><strong>Force-model fidelity vs. compile time.</strong> EGM2008 to high degree
inside a <code>jit</code> trace produces enormous compute graphs; staging strategies
(<code>static_argnums</code>, sharded force decomposition) are required.</li>
<li><strong>Reverse-mode through long integrations.</strong> Memory pressure on the
backward pass; the roadmap specifies optimal checkpointing thresholds.</li>
</ol>
"""},
],
"closing": """
<p>Companion to Nos. 02 and 04. Written immediately after the SPEPH monograph
in conversation
<a href="https://claude.ai/chat/2308b2c5-71af-4699-b330-b1624b01eef5">2308b2c5</a>.
The Mojo equivalent (No. 04) is structurally parallel — identical section
numbering, different stack.</p>
""",
},

# ============================================================
# 04 — Mojo Roadmap
# ============================================================
{
"num": 4,
"slug": "04-mojo-astrodynamics-roadmap",
"date": "2026-05-08",
"format": "LaTeX → PDF",
"length": "~24 pages",
"pdf": "04-mojo-astrodynamics-roadmap.pdf",
"pdf_available": False,
"title": "A Mojo-Native Differentiable, GPU-Native Astrodynamics Substrate",
"subtitle": "Layered Implementation Roadmap from Compiler Primitives to Operational Propagator",
"blurb": "Same problem as the JAX roadmap, different stack. Higher foundational cost; greater architectural control.",
"abstract_text": "The Mojo-stack roadmap. Layers JAX gets for free must be built — higher cost, greater architectural control.",
"abstract": """
<p>This monograph specifies a complete implementation roadmap for a high-fidelity
differentiable orbit propagator built on the Mojo programming language and the
broader Modular Platform, structured as a layered architecture from compiler-level
primitives upward to a production-grade propagator. The structural difference
from a JAX-equivalent roadmap is significant: where JAX provides production-grade
automatic differentiation, ODE integration, and ecosystem libraries on day one,
Mojo as of 2026 requires that several of these layers be built rather than
imported. This shifts the project shape from "compose existing components" to
"build the foundations, then compose them," with both a higher engineering burden
and a higher strategic upside in the form of greater architectural control and a
publishable contribution to the Mojo ecosystem.</p>
""",
"sections": [
{"heading": "Structural difference from JAX",
"body": """
<p>The intended audience is the technical lead who would own this work and is
willing to absorb the additional foundational effort in exchange for IR-level
optimization control, AOT deployment, and the language properties that
distinguish Mojo from Python-based alternatives.</p>

<p>The structure mirrors the parallel JAX-stack roadmap (No. 03); identical
sections in the two documents address the same engineering problem. The
comparative read is the point — every layer can be evaluated against its JAX
analog and decided on the explicit trade.</p>
"""},
{"heading": "What must be built that JAX gives away free",
"body": """
<ul>
<li><strong>Forward-mode AD over numerical primitives.</strong> Trait-driven via
<code>HasPrimal</code>/dual-number lifting; spec'd in detail in companion PRD v12.</li>
<li><strong>Reverse-mode AD for whole-trajectory adjoints.</strong> Graph IR with
explicit checkpointing; the heaviest engineering item below the propagator.</li>
<li><strong>An adaptive ODE integrator family.</strong> RK 8(7), Gauss-Jackson, and
a symplectic option; built against the GLMSpec abstraction so coefficients
are derived at compile time, not hand-coded.</li>
<li><strong>SIMD/GPU kernels for the dynamics RHS.</strong> Mojo's strengths show here;
this is what makes the foundational work worth it.</li>
<li><strong>BLAS/LAPACK shim or replacement.</strong> Decision point — wrap existing
C libraries via FFI, or write tile-based kernels in Mojo. The roadmap argues
for hybrid: wrap for linear algebra in the optimizer outer loop, native
kernels for the dynamics inner loop.</li>
</ul>
"""},
{"heading": "Strategic case",
"body": """
<p>The compounding upside: each foundational layer built is a publishable artifact
in a young ecosystem. A Mojo-native SOFA reimplementation, a Mojo orbit
propagator with SIMD/GPU benchmarks, a Mojo AD-enabled GLMSpec integrator
family — each lands in a domain where no comparable reference exists. The JAX
roadmap delivers operational capability; the Mojo roadmap delivers operational
capability <em>plus</em> three to five papers and a position in the ecosystem.</p>
"""},
],
"closing": """
<p>Third of three monographs from conversation
<a href="https://claude.ai/chat/2308b2c5-71af-4699-b330-b1624b01eef5">2308b2c5</a>
on 2026-05-08. Read in sequence with Nos. 02 (the technical case) and 03 (the
JAX-stack roadmap). The PRD v12 (No. 09) provides the architectural foundation
this roadmap assumes.</p>
""",
},

# ============================================================
# 05 — Cloud Cover Forecasting
# ============================================================
{
"num": 5,
"slug": "05-cloud-cover-forecasting",
"date": "2026-05-07",
"format": "LaTeX → PDF",
"length": "~40–50 pages",
"pdf": "05-cloud-cover-forecasting.pdf",
"pdf_available": False,
"title": "Total Cloud Cover Forecasting for EO Tasking",
"subtitle": "ML Weather Models from Keisler-2022 to GenCast, with a Differentiable-Pipeline Lens",
"blurb": "Where the ML-weather field actually is in 2026 — GraphCast, AIFS, GenCast, Aurora — what works for cloud cover, what runs on a 5060 Ti, and where the operational gaps are.",
"abstract_text": "ML weather forecasting for total cloud cover prediction, evaluated for satellite tasking applications.",
"abstract": """
<p>Cloud cover is not a normal weather variable. It is bounded $[0,1]$, strongly
bimodal (lots of 0s and 1s), spatially intermittent, and — critically — a
<em>diagnostic</em> in IFS rather than a prognostic state. ERA5's <code>tcc</code> is
itself a model output derived from cloud water/ice plus saturation, so any
model trained on it learns to mimic the IFS parameterization rather than ground
truth. Naïve MSE collapses toward 50% gray mush. The right architectural choices
— logit transform or beta head, CSI/Brier/HSS validation at operational
thresholds, calibration against geostationary truth — fall out of taking that
constraint seriously.</p>

<p>This monograph surveys the ML-weather landscape as of early 2026, with a focus
on what is actually useful for Earth-observation collection tasking on
constrained hardware.</p>
""",
"toc": [
    "Introduction and the cloud-cover-is-not-weather framing",
    "Where the field actually is: Keisler, GraphCast, AIFS, GenCast, Aurora, NeuralGCM",
    "Probabilistic vs deterministic for EO tasking",
    "Hardware and Compute Tiers (Tier 1 consumer through Tier 4 research clusters)",
    "Operational stack: multi-source fusion by lead time",
    "Calibration against observation truth vs reanalysis",
    "Local inference vs operational center inference",
    "The ∂LITE pattern: differentiable orbit ∘ geometry ∘ atmosphere",
    "TCC nowcasting: an open opportunity",
    "Notebook walk-through: ECMWF Open Data → in-between interpolation → ARCO ERA5 validation",
    "Appendix A: Variable-name reference across GRIB2 / ERA5 / ECMWF",
    "Appendix D: Skill metrics formulae (RMSE, MAE, Brier, CSI, HSS)",
],
"sections": [
{"heading": "Where the field actually is",
"body": """
<p>The honest landscape, with model · year · output · resolution · cadence · TCC
skill · open weights:</p>
<ul>
<li><strong>Keisler-2022</strong> · 2022 · Deterministic · 1° · 6h · demonstrated, weak · yes</li>
<li><strong>GraphCast</strong> · 2023 · Deterministic · 0.25° · 6h · decent · yes</li>
<li><strong>Pangu-Weather</strong> · 2023 · Deterministic · 0.25° · 1/3/6/24h · decent · yes</li>
<li><strong>AIFS (ECMWF)</strong> · 2024 · Deterministic + ENS · 0.25° · 6h ·
<em>best in class</em> · yes</li>
<li><strong>GenCast</strong> · 2024 · Probabilistic (diffusion ensemble) · 0.25° · 12h ·
strong, uncertainty-aware · yes</li>
<li><strong>Aurora</strong> · 2024 · Foundation, fine-tunable · 0.25° · 6h · strong · yes</li>
</ul>
<p>The MAUSAM paper (arXiv 2509.01879, Sep 2025) benchmarks all of these against
ground-based and geostationary observations — not just ERA5 — and finds AIFS
most consistent overall, with GraphCast and GenCast close behind. All beat
Keisler-2022 substantially. Errors against actual observations are 15–45%
larger than errors against reanalysis, which is the relevant gap for an EO
tasking application.</p>
"""},
{"heading": "Hardware tiers",
"body": """
<p><strong>Tier 1 (consumer, 8–16 GB VRAM)</strong> — RTX 5060 Ti (16 GB), 4060 Ti (16 GB).
Comfortable: Keisler-2022, GraphCast-small (1°), FourCastNet v1, Pangu (no TCC),
NeuralGCM (1.4°/2.8°). Tight: AIFS-single (0.25°, ~13 GB with flash-attn),
GraphCast (0.25°), GenCast (1°). Won't fit: GenCast (0.25°, needs 60 GB),
Aurora MR/HR.</p>
<p><strong>Tier 2 (prosumer, 24–48 GB)</strong> — A6000, 4090, 5090. Adds AIFS-single
comfortably, GraphCast at fp32, Aurora MR.</p>
<p><strong>Tier 3 (enterprise, 80 GB+)</strong> — A100/H100. GenCast 0.25° (~25 min/member),
Aurora HR (0.1°), training-from-scratch budgets.</p>
"""},
{"heading": "The ∂LITE pattern",
"body": """
<p>The differentiability of neural forecasters enables a class of inverse-problem
applications (sensitivity analysis, ML-native data assimilation,
gradient-based tasking optimization) that physics models cannot match. For SSA
and EO applications specifically, the ∂LITE pattern is the most promising
design space: compose differentiable orbit, geometry, and atmospheric operators;
optimize end-to-end for collection utility.</p>

<p>The proprietary IP is the calibration head and the historical
(forecast, observed-at-collect) archive, not the forecaster itself.</p>
"""},
{"heading": "TCC nowcasting: an open opportunity",
"body": """
<p>Most nowcasting work targets precipitation. For TCC nowcasting (0–6 h cloud
cover from geostationary imagery), practical options reduce to: (1) optical-flow
extrapolation of geostationary cloud mask (classic, robust, ~1 h skillful
horizon); (2) custom small ML model trained on (GOES L1B sequence) →
(GOES L2 cloud mask future); (3) persistence + climatology blend at the
lowest-effort end. <em>This is a real opportunity for proprietary EO-tasking IP:
there is no strong public TCC nowcaster as of early 2026.</em></p>
"""},
],
"closing": """
<p>Produced in conversation
<a href="https://claude.ai/chat/b47b9a50-630c-4bfd-a240-f41a59061091">b47b9a50</a>
on 2026-05-07. Accompanied by a Colab notebook
(<code>cloud_cover_forecasting.ipynb</code>, 26 cells) that exercises the full
ECMWF Open Data → temporal interpolation → ARCO ERA5 validation pipeline.</p>
""",
},

# ============================================================
# 06 — Viewshed
# ============================================================
{
"num": 6,
"slug": "06-viewshed-azel-lookup",
"date": "2026-04-23",
"format": "LaTeX → PDF",
"length": "~23 pages, 557 KB",
"pdf": "06-viewshed-azel-lookup.pdf",
"pdf_available": False,
"title": "Precomputed Azimuth–Elevation Horizon Masks for Satellite Visibility over Terrain",
"subtitle": "A Spatial-Coherence-Exploiting Lookup Structure",
"blurb": "A complete methodology for $(\\lambda,\\phi) \\mapsto \\mathcal{H}$ lookup tables, with a far/near decomposition theorem and closed-form error bounds.",
"abstract_text": "Methodology for constructing a lookup table mapping a geodetic query point to its terrain-induced az-el mask, with provable error bounds.",
"abstract": """
<p>We present a complete methodology for constructing a lookup table that maps a
geodetic query point $(\\lambda, \\phi)$ to the terrain-induced azimuth–elevation
mask governing satellite visibility from that location. The mask
$\\mathcal{H}_{\\lambda\\phi}: S^1 \\to [-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}]$
encodes, for every azimuth $\\varphi$, the minimum elevation above which the sky
is unobstructed by terrain. A satellite at topocentric direction
$(\\varphi^*, \\eta^*)$ is visible iff $\\eta^* > \\mathcal{H}_{\\lambda\\phi}(\\varphi^*)$.</p>

<p>Naïve per-query computation on a DEM of $n$ cells costs $\\Theta(n^{1.5})$ per
point, $\\Theta(n^{2.5})$ for the all-cells horizon. We review the classical R2,
R3, and XDraw viewshed algorithms, Stewart's $O(n \\log n)$ all-points horizon
algorithm, and the sDEM / band-of-sight data relocation technique of Tabik et al.,
then build a lookup structure that exploits the strong spatial coherence of
horizons between nearby observers.</p>

<p>The central observation is a <em>far/near decomposition</em>: the horizon at a
point $\\boldsymbol{p}$ is the pointwise maximum of a <em>far</em> component,
governed by distant terrain and nearly constant over tiles of diameter
$\\ll R_{\\max}$, and a <em>near</em> component, which varies rapidly but can be
computed on demand from a small local window. Combined with low-rank (PCA)
per-tile residuals and piecewise-linear azimuthal encoding, total storage drops
1–2 orders of magnitude relative to naïve per-cell storage, with bounded error
characterised in closed form.</p>
""",
"toc": [
    "Introduction and problem statement",
    "Geometric preliminaries: ECI→ECEF→ENU, WGS-84, the $k_{\\text{ref}}$-Earth-radius model",
    "Classical viewshed algorithms: R2, R3, XDraw, complexities",
    "Total-horizon computation: Stewart's backward sweep, Tabik sDEM / band-of-sight",
    "Spatial coherence analysis: the far/near decomposition theorem with Lipschitz bound",
    "Lookup structure: hierarchical tiles, three compression axes, query algorithm with error bound",
    "Satellite ECI → topocentric azimuth-elevation pipeline",
    "Refraction and curvature corrections for VHF–Ka radio and optical sensing",
],
"sections": [
{"heading": "Problem statement",
"body": """
<p>Given a digital elevation model $\\mathcal{T}: \\mathcal{D} \\to \\mathbb{R}$
on a bounded geographic domain $\\mathcal{D}$ with cell size $\\Delta$ and a
maximum sensing range $R_{\\max}$, construct a data structure $\\mathcal{M}$
supporting queries</p>
<p>$$\\mathcal{M}(\\lambda, \\phi) \\longmapsto \\widehat{\\mathcal{H}}_{\\lambda\\phi}(\\cdot),
\\qquad \\widehat{\\mathcal{H}}_{\\lambda\\phi}: S^1 \\to \\mathbb{R},$$</p>
<p>such that
$\\|\\widehat{\\mathcal{H}}_{\\lambda\\phi} - \\mathcal{H}_{\\lambda\\phi}\\|_\\infty \\le \\varepsilon_{\\text{tol}}$
for every $(\\lambda,\\phi) \\in \\mathcal{D}$, using as little storage and query
time as possible.</p>
"""},
{"heading": "Contributions",
"body": """
<ul>
<li>A uniform mathematical formulation admitting curvature and refraction in
closed form, relating the az-el mask to the classical viewshed.</li>
<li>A consolidated exposition of R2, R3, XDraw, Stewart's sweep, and Tabik's
sDEM with precise complexities on a common grid model.</li>
<li>A quantitative analysis of spatial coherence yielding a rigorous far/near
decomposition theorem (Theorem 5.1) with explicit Lipschitz bound
$|\\Delta\\mathcal{H}^{\\text{far}}| \\le \\delta(1+M)/R_n + \\text{curvature term}$.</li>
<li>A lookup structure built from hierarchical tiles carrying compressed
far-horizons plus lazy near-horizon evaluation, with provable error bounds.</li>
<li>End-to-end specification for converting orbital state to az-el and querying
the mask, including refraction and curvature corrections appropriate for
VHF–Ka radio and optical sensing.</li>
</ul>
"""},
{"heading": "The gap this fills",
"body": """
<p>The viewshed literature divides into (i) single-observer viewshed algorithms
(R2/R3 of Franklin &amp; Ray, XDraw of Wang et al.), (ii) all-points total-viewshed /
horizon-map algorithms (Stewart, De Floriani &amp; Magillo, Tabik et al.,
Sanchez-Fernandez et al.), and (iii) GPU / I/O-efficient implementations
(Cauchi-Saunders &amp; Lewis, Fishman et al., Qarah). The satellite-specific
specialisation appears in mission-analysis tools — AGI STK's <code>AzElMask</code> /
<code>TerrainMask</code> constraints, MATLAB's Satellite Communications Toolbox
visibility-mask workflow, ground-station design literature. Solar-resource and
shading work is structurally the same problem. <em>None of these, to the author's
knowledge, addresses the offline construction of a compressed
$(\\lambda,\\phi) \\mapsto \\mathcal{H}$ lookup using formal far/near
decomposition with closed-form error bounds.</em> That is the gap.</p>
"""},
],
"closing": """
<p>Produced in conversation
<a href="https://claude.ai/chat/19824ab5-fc9e-454c-82b3-8f7dae029bdb">19824ab5</a>
on 2026-04-23 alongside the broader viewshed-compute Python package. Compiled
cleanly (0 errors) after working through several macro-conflict issues during
the run — accidental backspace bytes from <code>\\b*</code> macros and a few
<code>\\Rearth</code>/<code>\\Return</code> collisions.</p>
""",
},

# ============================================================
# 07 — TLE from UCT
# ============================================================
{
"num": 7,
"slug": "07-tle-from-uct-pipeline",
"date": "2026-04-09",
"format": "LaTeX → PDF",
"length": "~41 pages, AMS style",
"pdf": "07-tle-from-uct-pipeline.pdf",
"pdf_available": False,
"title": "From Uncorrelated Tracks to TLEs",
"subtitle": "A Comprehensive Mathematical Pipeline with Provider-Specific Implementations",
"blurb": "Time systems, two-body mechanics, the IOD family, batch WLS, Kalman variants, SGP4/SDP4, and deep-dives into 18 SDS, LeoLabs, Slingshot, and ExoAnalytic.",
"abstract_text": "End-to-end mathematical treatment from UCT observations through TLE packaging, with provider-specific implementation details.",
"abstract": """
<p>A complete, derivation-first treatment of the mathematical pipeline that turns
uncorrelated observation tracks into the Two-Line Element sets that operational
SDA systems publish. Every equation is derived or stated with full variable
definitions; no step is skipped. The companion ambition is to document, in
exhaustive detail, how the four major commercial and government SDA providers
actually implement this pipeline in practice: the 18th Space Defense Squadron
(formerly 18 SPCS), LeoLabs, Slingshot Aerospace, and ExoAnalytic Solutions.</p>
""",
"toc": [
    "Part I — Mathematical Foundations: time systems, reference frames, two-body mechanics",
    "Part II — The Pipeline: track correlation, admissible region theory",
    "Initial Orbit Determination: Laplace, Gauss, Gooding, Lambert (Battin/Gooding/Izzo), Herrick–Gibbs",
    "Batch Weighted Least Squares: full Jacobian derivations",
    "Sequential filtering: EKF, UKF, square-root variants",
    "SGP4 / SDP4: complete algorithm with all constants",
    "The Vallado–Crawford–Hujsak–Kelso TLE-fit procedure",
    "TLE format and checksum mechanics",
    "Uncertainty quantification end-to-end",
    "Part III — Provider Implementations: 18 SDS",
    "LeoLabs",
    "Slingshot Aerospace",
    "ExoAnalytic Solutions",
    "Part IV — Comparative Analysis and Open Problems",
    "Comprehensive bibliography",
],
"sections": [
{"heading": "Scope and approach",
"body": """
<p>Full pipeline; AMS article style; all available sources, including open
literature (AMOS/AAS/AIAA papers, patents, SBIR abstracts, press),
government documents where available (SDA, SSC TTPs, JFSCC, CSpOC SOPs), and
direct vendor materials.</p>

<p>The construction is uncompromising on derivations. Where conventional
treatments collapse "differentiate and solve" into a sentence, this monograph
expands to the explicit Jacobian — partials of range, range-rate, and angles
with respect to the six-element state — and tracks every approximation
introduced along the way.</p>
"""},
{"heading": "Initial Orbit Determination, complete",
"body": """
<p>Laplace, Gauss, Gooding, Lambert (via Battin's universal-variable formulation,
Gooding's iterative scheme, and Izzo's elegant rewrite), and Herrick–Gibbs are
each derived from first principles, with worked numerical examples and
discussion of which method to use under which observation geometry. The
admissible region machinery — Tommei, Milani, Rossi — is presented in its
modern form, including the connection to attributable orbit determination.</p>
"""},
{"heading": "SGP4 and the TLE fit",
"body": """
<p>The complete SGP4/SDP4 algorithm is reproduced with all constants — the WGS72
choice (not WGS84, despite the name of the latter being more familiar) is
non-negotiable for parity with operational systems. The Vallado–Crawford–Hujsak–Kelso
fit procedure converts a high-fidelity ephemeris back into a TLE by iteratively
adjusting the mean elements so the SGP4 ephemeris matches the truth ephemeris
in least-squares sense over the fit span.</p>

<p>The checksum mechanics (the last digit of each TLE line) are reproduced with
the modulo-10 algorithm.</p>
"""},
{"heading": "Provider deep-dives",
"body": """
<p>For each of 18 SDS, LeoLabs, Slingshot, and ExoAnalytic: the architecture as it
can be reconstructed from open materials, the sensor mix that feeds the
pipeline, the filtering and IOD choices that distinguish them, the public-facing
products (UCT catalogs, conjunction screening services, SSA-as-a-service APIs),
and what is provably <em>not</em> in the open record. The intent is not to
out the providers but to map the design space against the math in Parts I–II.</p>
"""},
],
"closing": """
<p>Final LaTeX is ~2800 lines; PDF is 41 pages. Produced in conversation
<a href="https://claude.ai/chat/1349ca6e-2eee-4531-9d4d-78444e05057a">1349ca6e</a>
on 2026-04-09 after a research phase across 150+ publications. Required three
<code>pdflatex</code> passes for full cross-reference resolution;
<code>xcolor</code> with <code>[dvipsnames]</code> must precede <code>hyperref</code>
to support mixed color specifications; stacked math accents
(<code>\\dot{\\hat{\\boldsymbol{L}}}</code>) need helper macros to dodge
<code>\\macc@adjust</code> errors.</p>
""",
},

# ============================================================
# 08 — Orbital Propagation & UQ Literature Review
# ============================================================
{
"num": 8,
"slug": "08-orbital-propagation-uq-literature-review",
"date": "2026-04-01",
"format": "Markdown",
"length": "~150 publications, 12 areas",
"pdf": "08-orbital-propagation-uq-literature-review.pdf",
"pdf_available": False,
"title": "Orbital Propagation and Uncertainty Quantification",
"subtitle": "A 2024–2026 Literature Review",
"blurb": "Twelve technical areas, ~150 recent publications. The unexploited gaps: operator splitting for satellite dynamics, semiglobal Chebyshev×Taylor, normalizing flows for orbital uncertainty.",
"abstract_text": "Comprehensive review of 2024-2026 advances in orbital propagation and uncertainty quantification, with gap analysis.",
"abstract": """
<p>The most promising advances in orbital propagation converge on three themes:
adaptive-order Taylor integration reaching production maturity, differential
algebra methods proving their operational viability, and an unexploited gap in
operator splitting for satellite dynamics. This review spans 12 technical areas
across ~150 recent publications and identifies several combinations and
overlooked techniques that could genuinely exceed the state of the art.</p>

<p>The most striking finding is that operator splitting applied to artificial
satellite dynamics — despite its natural fit to the near-integrable
Kepler-plus-perturbation structure — remains essentially unexplored, while
Koopman spectral methods, often assumed niche, have exploded into a 15–20
paper subfield in the last two years alone.</p>
""",
"toc": [
    "Taylor integrators (heyoka, Tan/Smith/Rackauckas adaptive order)",
    "Modified Chebyshev-Picard Iteration (Junkins, Woollands, Bai)",
    "Differential Algebra and Jet Transport (Massari, Wittig, Armellin, Di Lizia)",
    "Koopman operator methods for orbital mechanics",
    "Operator splitting and exponential integrators (the unexplored gap)",
    "Neural ODE / differentiable propagators (dSGP4, ThermoNET, ML-∂SGP4)",
    "Scientific foundation models and their limitations (Vafa et al., Liu et al.)",
    "Uncertainty propagation beyond Gaussian (GBEES, particle flow, normalizing flows)",
    "Symplectic and geometric integrators",
    "GPU-accelerated propagation (jaxsgp4)",
    "Geometric / Clifford algebra applications",
    "The Mojo programming language ecosystem for astrodynamics",
],
"sections": [
{"heading": "Taylor integrators have crossed the operational threshold",
"body": """
<p>The heyoka ecosystem (Biscani &amp; Izzo) has evolved from a research-grade Taylor
integrator into an operational Earth-orbit propagation framework. As of
<code>heyoka.py v7.10.1</code>, it supports EGM2008 geopotential, NRLMSISE-00 and
JB-08 atmospheric models, IAU2000/2006 precession-nutation, Earth Orientation
Parameters, ICRS/ITRS/TEME frame transformations, and VSOP2013/ELP2000
ephemerides. The LLVM JIT compilation pipeline exploits AVX-512/Neon SIMD, and
batch mode processes multiple initial conditions simultaneously with 2–8×
SIMD speedup. High-order variational equations — computing arbitrary-order flow
derivatives while exploiting Schwarz symmetries — are built in, and Neural ODE
support enables embedding learned atmospheric models (ThermoNET) directly in
the equations of motion.</p>

<p>The February 2026 paper by Tan, Smith, and Rackauckas (arXiv:2602.04086)
introduces the first comprehensive adaptive time-and-order Taylor algorithm for
general ODEs. Using Julia's multiple dispatch and TaylorDiff.jl, they generate
optimized recursive code via symbolic-numeric computing — no user-facing macros
or code rewriting required, unlike <code>TaylorIntegration.jl</code>'s
<code>@taylorize</code>.</p>
"""},
{"heading": "Proposed advances identified",
"body": """
<ul>
<li><strong>Operator splitting for satellite dynamics</strong> as a genuine blind
spot despite mature mathematical infrastructure from planetary dynamics.</li>
<li><strong>A semiglobal Chebyshev-in-time × Taylor-in-state polynomial
propagator</strong> combining MCPI and differential algebra — unrealized despite
both components being mature.</li>
<li><strong>Koopman–exponential integrator fusion</strong> as an unexplored combination.</li>
<li><strong>GBEES on GPU</strong> for full-PDF uncertainty propagation enabling
real-time non-Gaussian filtering.</li>
<li><strong>Normalizing flows for orbital uncertainty</strong> as an open frontier
where the natural geometry (e.g., on the orbital element manifold) has not yet
been exploited.</li>
</ul>
"""},
],
"closing": """
<p>Produced in conversation
<a href="https://claude.ai/chat/09b8bef9-734e-4ae9-9322-f54cabbb3a78">09b8bef9</a>
on 2026-04-01 via an extended research task across 12 areas. Domain terminology
indexed: SGP4/dSGP4, EGM2008, NRLMSISE-00/JB-08, TPSA, DACE, MCPI, DA, ADS,
WH/WHFast/TRACE, GMM, PCE, GBEES, EDMD, CR3BP, NRHO, heyoka.</p>
""",
},

# ============================================================
# 09 — Mojo PRD v12
# ============================================================
{
"num": 9,
"slug": "09-mojo-hybrid-architecture-prd-v12",
"date": "2026-03-20",
"format": "Markdown",
"length": "~17,300 words; 2,235 lines; 20 sections + 9 appendices",
"pdf": "09-mojo-hybrid-architecture-prd-v12.pdf",
"pdf_available": False,
"title": "Hybrid Architecture PRD: Trait-Driven Scientific Computing System",
"subtitle": "Version 12 — Static Specialization as Primary, Graph IR for Dynamic Concerns",
"blurb": "Traits + AlgebraSpec + comptime specialization + graph for dynamic concerns. The architecture for a unified Mojo scientific computing library.",
"abstract_text": "Product requirements for a multi-paradigm scientific computing system in Mojo, unifying algebraic types, AD, integrators, and backends.",
"abstract": """
<p>This document specifies a multi-paradigm scientific computing system built in
Mojo. The system unifies algebraic number types (Clifford, exterior, dual, jet,
quaternion, and others), automatic differentiation, numerical integrators, and
backend execution under a single coherent architecture. The core architectural
thesis is:</p>

<p style="text-align:center;font-style:italic">Traits + AlgebraSpec + Comptime Specialization + Graph for Dynamic Concerns</p>

<p>This is a trait-driven, statically-specialized system. The primary execution
path generates specialized kernels at compile time from method specifications
and algebra specifications. A runtime graph IR exists only for dynamic
orchestration and reverse-mode AD.</p>
""",
"toc": [
    "Vision &amp; scope",
    "Mathematical foundations",
    "Trait layer specification (the center of gravity)",
    "Algebra specs &amp; generated types",
    "Compilation model: static / planned / dynamic three-tier execution",
    "Compile-time IR &amp; optimization passes",
    "Runtime graph: scope &amp; boundaries (explicitly narrowed)",
    "AD architecture: forward algebraic + reverse graph",
    "Backend &amp; storage",
    "Validation stack (property tests, Lean export, Mathlib4 alignment)",
    "Implementation roadmap (16 milestones)",
    "Appendix A — Code examples and benchmarks",
    "Appendix B — Mojo alignment notes",
    "(plus seven more appendices)",
],
"sections": [
{"heading": "The architectural resolution",
"body": """
<p>The PRD resolves a long-running debate between a graph-IR-first approach and a
comptime-first approach in favor of a three-tier model (static / planned /
dynamic). Key structural decisions:</p>
<ul>
<li><strong>GLMSpec with coefficient matrices (A, U, B, V) as the unifying
integrator abstraction</strong> — subsumes RK, BDF, multistep, and peer methods.</li>
<li><strong>A domain-specific CAS built from the same AlgebraSpec building blocks</strong>
feeding a CAS → Lean → comptime verified pipeline.</li>
<li><strong>Algebraic lifting as a general enrichment mechanism</strong> covering AD,
covariance propagation, polynomial chaos, and interval validation.</li>
<li><strong>Comptime-generated orthogonal polynomial families</strong> (Hermite,
Legendre, Laguerre, Chebyshev, Jacobi) enabling PCESpec as a legitimate
AlgebraSpec for uncertainty quantification.</li>
</ul>
"""},
{"heading": "Scoping decisions",
"body": """
<ul>
<li>Orbit-type-aware propagation and polynomial event detection belong in
<em>consumer packages</em>, not the core library.</li>
<li>The CAS should be <em>narrow and focused</em> — exact rational arithmetic,
spec-derived rewriting, GLM coefficient derivation, Lean export — not a
general-purpose CAS.</li>
<li>PDE support is a consumer layer built on top of the core.</li>
<li>The library is positioned as a <em>backbone for astrodynamics tools</em>
(STK / GMAT / Orekit / heyoka successors) and high-fidelity scientific
simulation, not for real-time physics engines like NVIDIA Newton.</li>
</ul>
"""},
{"heading": "Reference implementations studied",
"body": """
<p>DifferentialEquations.jl (problem/algorithm separation, sensitivity-analysis
crossover point), JAX/XLA (staging artifact model,
<code>static_argnums</code>), Diffrax (adaptive stepping vs tracing tension),
Enzyme (reverse-mode performance ceiling), DiGeo
(<code>HasCustomAdjoint</code> pattern for non-smooth discrete operations;
parallel transport as geodesic byproduct), TaylorIntegration.jl (jet
coefficient propagation), Mathlib4 (Lean proof foundation).</p>

<p>The trait hierarchy includes a <code>HasCustomAdjoint</code> trait covering
DiGeo-style proxy gradients for discrete geometric operations, implicit
function theorem adjoints for nonlinear solves, continuous adjoint methods for
ODE trajectory sensitivity, and any future operation where automatic AD is
insufficient.</p>
"""},
],
"closing": """
<p>Twelfth iteration; the v11 hybrid PRD ran 6,900 lines as "geological strata"
that mixed graph-first and comptime-first framings. v12 is the rewrite around
the hybrid architecture as primary. Produced in conversation
<a href="https://claude.ai/chat/73f1973e-ca55-443d-b04f-a07967743ba3">73f1973e</a>
on 2026-03-20. Companion to the JAX and Mojo roadmap monographs (Nos. 03 and 04)
which assume this architectural foundation.</p>
""",
},

]
