#version 440 core

#include "math_nd.glsl"

layout(location=M_LOCATION(0,0)) in vec4 position;
layout(location=M_LOCATION(1,0)) in vec4 texcoord;
layout(location=M_LOCATION(1,1)) in vec4 color;

uniform matN model_nd;
uniform matN view_nd;
uniform matN projection_nd;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out VertexData {
    vec4 position;
    vec4 texcoord;
    vec4 color;
} vs;


struct Vertex4 {
    vec4 position;
    mat4 basis;
    vec4 texture;
    vec4 color;
};

layout(std430, binding = 1) buffer VertexData {
    Vertex4 vertices[];
};

void main()
{
    vs.position = model * vertices[gl_VertexID].position;
    vs.color = color;
    vs.texcoord = texcoord;
   
    gl_Position = projection * view * vs.position;
}
