# 🐢 regulation_turtle

> Régulation de trajectoire avec ROS 2 — contrôle par waypoints pour turtlesim

![ROS2](https://img.shields.io/badge/ROS_2-jazzy-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![License](https://img.shields.io/badge/Licence-MIT-lightgrey?style=flat-square)

---

## Installation

### 1. Créer le workspace ROS

```sh
mkdir -p ~/turtle_ws/src
cd ~/turtle_ws
colcon build
```

### 2. Cloner les dépôts

```sh
cd src
git clone https://github.com/Kramoth/regulation_turtle.git
git clone https://github.com/Kramoth/turtle_interfaces.git
```

### 3. Build & source

```sh
cd ..
colcon build
source install/setup.bash
```

---

## Lancer les noeuds

Ouvrir **3 terminaux** séparés :

**Terminal 1** — Simulateur
```sh
ros2 run turtlesim turtlesim_node
```

**Terminal 2** — Noeud de régulation
```sh
source ~/turtle_ws/install/setup.bash
ros2 run regulation_turtle set_way_point_node \
  --ros-args -p Kpl:=0.5 -p Kp:=20.0
```

**Terminal 3** — Client waypoint
```sh
source ~/turtle_ws/install/setup.bash
ros2 run regulation_turtle set_way_point_client_node
```

### Paramètres

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| `Kpl` | Gain proportionnel linéaire | `0.8` |
| `Kp`  | Gain proportionnel angulaire | `5.0` |
