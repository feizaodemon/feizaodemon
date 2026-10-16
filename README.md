<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-en-dark.svg">
  <img alt="Xiaowei Rong: robot software, control, full-stack tools" src="assets/banner-en-light.svg" width="100%">
</picture>

<p align="center"><b>English</b> · <a href="https://github.com/feizaodemon/feizaodemon/blob/main/README.zh-CN.md">简体中文</a></p>

I build robot software end to end: recognition and supervision logic, Cartesian and torque controllers on Franka arms, and the experiments and tests that show whether they work. When a spreadsheet stops being enough, I build the tool myself.

## Featured project

### [Magnetic Trajectory Robot Interface](https://github.com/feizaodemon/magnetic-trajectory-robot-interface)

Draw a symbol on a magnetic board or with the mouse. The system recognizes it, the operator confirms it, and only then does the robot run the matching task.

<a href="https://github.com/feizaodemon/magnetic-trajectory-robot-interface"><img src="assets/mtri-task-gazebo.gif" alt="Draw a symbol, recognize it, confirm it, and the Gazebo robot runs the task" width="100%"></a>

<p>
  <img alt="Leave-one-out Top-1: 100%" src="https://img.shields.io/badge/leave--one--out%20Top--1-100%25-0f9488?style=flat-square">
  <img alt="Recognition: about 83 ms per query" src="https://img.shields.io/badge/recognition-~83%20ms%20%2F%20query-0f9488?style=flat-square">
  <img alt="Template bank: 124 templates, 8 symbols" src="https://img.shields.io/badge/bank-124%20templates%20%C2%B7%208%20symbols-0f9488?style=flat-square">
  <img alt="CI: 8 jobs including a headless Gazebo smoke test" src="https://img.shields.io/badge/CI-8%20jobs%20incl.%20Gazebo%20smoke-c47a00?style=flat-square">
</p>

- **Gesture to task.** A DTW template bank ranks pen or mouse strokes, with confidence and margin gates that reject unclear input. Five alternative recognizers are benchmarked against it under noise, rotation and truncation.
- **Confirmation-gated control.** Recognition, confirmation, dispatch and execution are separate ROS nodes. Only the dispatcher can command the robot, and only after an explicit confirm.
- **One teleop core, two robots.** A C++ Cartesian core with damped-least-squares IK drives both a Gazebo Panda and a Franka FR3 adapter.

ROS1 Noetic · Python · C++ · Gazebo · Docker → [Design decisions](https://github.com/feizaodemon/magnetic-trajectory-robot-interface/blob/main/docs/DESIGN_DECISIONS.md)

## More work

<sub>These repositories are private (team, coursework or personal data), so they are described here instead of linked.</sub>

<table>
<tr>
<td width="33%" valign="top">

**GP torque compensation**<br>
<sub>Team research project · ROS 2 · Python</sub>

Learning the residual joint torque of a Franka Panda with Gaussian processes and feeding a small, clipped share back into an impedance controller.

My part: code development, including the experiment switches that made frozen-GP tests possible; real-robot testing in the lab; a staged test programme with a plan and report for each stage; and the offline analysis that compared the online GPs with a historical residual database.

</td>
<td width="33%" valign="top">

**Job-search workbench**<br>
<sub>Personal tool · TypeScript · Fastify · React · SQLite</sub>

A self-hosted tracker I use every day instead of a spreadsheet. Jobs and applications are kept separate, and every status change is written as an event in the same transaction.

34 API routes, 420+ test cases in CI, and a Chrome extension that only saves jobs and asks for just 3 permissions.

</td>
<td width="33%" valign="top">

**Robot manipulation coursework**<br>
<sub>Group projects · ROS 2 · C++</sub>

Four Franka and UR5e projects. In each one I worked on the code and on the real-robot tests.

- task-priority IK under a remote-center-of-motion constraint, run on a real FR3
- hand-taught trajectories replayed by a custom joint-impedance torque controller
- a vision-triggered button press
- an SVG drawing study explaining 77 s simulated vs. about 180 s real cycle time

</td>
</tr>
</table>

## Toolbox

<p>
  <img alt="ROS" src="https://img.shields.io/badge/ROS%20%2F%20ROS%202-22314E?style=flat-square&logo=ros&logoColor=white">
  <img alt="C++" src="https://img.shields.io/badge/C%2B%2B-00599C?style=flat-square&logo=cplusplus&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="Gazebo" src="https://img.shields.io/badge/Gazebo-F58113?style=flat-square">
  <img alt="MuJoCo" src="https://img.shields.io/badge/MuJoCo-4B5563?style=flat-square">
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white">
  <img alt="React" src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB">
  <img alt="Fastify" src="https://img.shields.io/badge/Fastify-000000?style=flat-square&logo=fastify&logoColor=white">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white">
  <img alt="GitHub Actions" src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white">
</p>
