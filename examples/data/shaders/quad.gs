#version 440 core

//#include "common.glsl"

layout(points) in;
layout(triangle_strip, max_vertices=4) out;

out VertexData { vec4 position; vec4 tex_coord; vec4 color; } gs;

//#include "uniforms.glsl"

uniform mat4 model = mat4(1.0);
uniform mat4 view = mat4(1.0);
uniform mat4 projection = mat4(1.0);

uniform mat4 model_view = mat4(1.0);
uniform mat4 view_projection = mat4(1.0);
uniform mat4 model_view_projection = mat4(1.0);

uniform mat4 tex_coord_transform = mat4(1.0);
uniform mat4 color_transform = mat4(1.0);


void make_vertex(vec4 position, vec4 tex_coord, vec4 color) {
    gs.position = position; //position_transform *
    gs.tex_coord = tex_coord_transform * tex_coord;
    gs.color = color; //color_transform *
    gl_Position = gs.position;
    EmitVertex();
}

void make_quad(vec4 position, vec4 tex_coord, vec4 color) {
    make_vertex(position + vec4(-1,-1,0,0), tex_coord + vec4(0,1,0,0), color);
    make_vertex(position + vec4(+1,-1,0,0), tex_coord + vec4(1,1,0,0), color);
    make_vertex(position + vec4(-1,+1,0,0), tex_coord + vec4(0,0,0,0), color);
    make_vertex(position + vec4(+1,+1,0,0), tex_coord + vec4(1,0,0,0), color);
    EndPrimitive();
}

void main() {
    make_quad(vec4(0,0,0,1), vec4(0,0,0,1), vec4(1.0));
}
