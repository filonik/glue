#version 440 core

in VertexData { vec4 position; vec4 tex_coord; vec4 color; } gs;

uniform vec3 iResolution = vec3(1280.0, 720.0, 1.0);
uniform float iTime = 0.0;

out vec4 frag_color;

#include "shadertoy/clover.glsl"
//#include "shadertoy/fractal_tiling.glsl"
//#include "shadertoy/overly_satisfying.glsl"

void main()
{
    //mainImage(frag_color, gl_FragCoord.xy);
    mainImage(frag_color, gs.tex_coord.st * iResolution.xy);
}
