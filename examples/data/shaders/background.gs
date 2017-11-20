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


void make_vertex(vec4 position, vec4 tex_coord, vec4 color) {
    gs.position = position; //position_transform *
#if GLANCE_BACKGROUND_CUBE
    gs.tex_coord = inverse(projection * mat4(mat3(model_view))) * position;
#else
    gs.tex_coord = tex_coord; //tex_coord_transform *
#endif
    gs.color = color; //color_transform *
    gl_Position = gs.position;
    EmitVertex();
}

void make_quad(vec4 position, vec4 tex_coord, vec4 color) {
    make_vertex(position + vec4(-1,-1,0,0), tex_coord + vec4(0,0,0,0), color);
    make_vertex(position + vec4(+1,-1,0,0), tex_coord + vec4(1,0,0,0), color);
    make_vertex(position + vec4(-1,+1,0,0), tex_coord + vec4(0,1,0,0), color);
    make_vertex(position + vec4(+1,+1,0,0), tex_coord + vec4(1,1,0,0), color);
    EndPrimitive();
}

void main() {
    make_quad(vec4(0,0,0,1), vec4(0,0,0,1), vec4(1.0));
}
