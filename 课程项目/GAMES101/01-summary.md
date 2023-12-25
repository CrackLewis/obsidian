
[link](https://sites.cs.ucsb.edu/~lingqi/teaching/resources/GAMES101_Lecture_01.pdf)

[course website](https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html)

[homeworks](https://games-cn.org/forums/topic/allhw/)

## intro

**what is computer graphics**:
the use of computers to synthesize and manipulate visual information.

**why computer graphics**:
- applications: video games, movies, animations, design, visualization, vr, ar, digital illustration, simulation, gui, typography（字体排印学）
- fundamental intellectual challenges
	- creates and interacts with realistic virtual world
	- requires understanding of all aspects of physical world
	- new computing methods, displays, technologies
- technical challenges
	- math of (perspective) projections, curves, surfaces
	- physics of lightning and shading
	- representing & operating shapes in 3D
	- animation & simulation

## course topics

- rasterization（光栅化）
	- project geometry primitives (3D triangles / polygons) onto the screen
	- break projected primitives into fragments (pixels)
	- gold standard in video games (real-time applications)
- curves and meshes（曲线和网格）
	- how to represent geometry in computer graphics
- ray tracing
	- shoot rays from the camera through each pixel
		- calc intersection and shading
		- continue to bounce the rays until they hit light sources
	- gold standard in animations & movies (offline applications)
- animation & simulation
	- key-frame animation
	- mass-spring system（弹簧质点系统）

![[Pasted image 20231225151720.png]]
(rasterization)

**this course does NOT talk about**: (but all of these should be learnt after the course)
- OpenGL/DirectX/Vulkan
- the syntax of shaders
- any form of graphics APIs
- 3D modeling (using Maya/3DS MAX/Blender) or VR/game devs (using Unity)
- CV or DL topics (such as XXX-GAN, XXX-Diffusion, XXX-Transformer)

**differences between CG and CV**:
![[Pasted image 20231225153106.png]]
CV & CG both have no clear boundaries and can't be easily defined

## course logistics

**general info**:
- modern course: comprehensive, no hardware programming, pace & content subject to change
- [course website](https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html)
- reference: [[Fundamentals of Computer Graphics, Fourth Edition (Steve Marschner, Peter Shirley) (Z-Library).pdf]]
- [bbs](https://games-cn.org/forums/forum/graphics-intro/)

## abbrevs

- CV->computer vision
- CG->computer graphics
- CarCo->cartesian coordinates
- Prj->projection
- HmCo->homogeneous coordinates
- TrL->linear transform
- TrS->translation
- ...