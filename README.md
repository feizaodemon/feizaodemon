# Robotics software · control · full-stack tools

I build robot software end to end: recognition and supervision logic, Cartesian and torque controllers on Franka arms, and the experiments and tests that show whether they work. I also build my own tools when a spreadsheet stops being enough.

## Projects

### [Magnetic Trajectory Robot Interface](https://github.com/feizaodemon/magnetic-trajectory-robot-interface) · ROS1 · Python · C++

Draw a symbol, confirm it, and the robot runs the matching task. A DTW template bank reaches **100% leave-one-out Top-1** on 124 templates over 8 symbols at about **83 ms per query**, behind a confirmation-gated command path; one C++ Cartesian teleop core drives both Gazebo and a Franka FR3 adapter. **8 CI jobs** including a headless Gazebo smoke test.
→ [Design decisions](https://github.com/feizaodemon/magnetic-trajectory-robot-interface/blob/main/docs/DESIGN_DECISIONS.md)

### GP torque compensation (team research project, private) · ROS 2 · Python

Learning the residual joint torque of a Franka Panda with Gaussian processes. A frozen GP at scale 0.3 lowered the torque residual RMS on **all 7 joints (−13.6 % to −74.9 %)** while tracking error stayed level (3.96 mm → 3.72 mm), in a single real-robot run. My part: the experiment switches, the staged test programme with a plan and report per stage, and the offline analysis that found a historical residual database predicts the residual far better than the online GPs (RMSE 0.394 vs. 1.005).

### Job-search workbench (private) · TypeScript · Fastify · React · SQLite

A self-hosted tracker I use every day instead of a spreadsheet: jobs and applications kept separate, every status change written as an event in the same transaction, and a Chrome extension that only saves jobs with 3 permissions. 34 API routes, 420+ test cases in CI.

### Robot manipulation coursework (group projects, private) · ROS 2 · C++

Four Franka / UR5e projects: task-priority IK under a remote-center-of-motion constraint, run on a real FR3; kinesthetic teaching replayed by a custom joint-impedance torque controller with torque-rate limiting; a vision-triggered button press; and an SVG drawing study that explains a 77 s simulated vs. about 180 s real cycle time.

## Tools I use

ROS / ROS 2 · C++ · Python · Gazebo · MuJoCo · Franka · TypeScript · React · Fastify · SQLite · Docker · GitHub Actions
