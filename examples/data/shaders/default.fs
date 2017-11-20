#version 440 core

#include "vertices_nd.glsl"

layout(location=0) out vec4 frag_color;

in VertexData { Vertex4 vertex; } gs;

void main()
{
    frag_color = gs.vertex.color; //vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
