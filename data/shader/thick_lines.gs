#version 400 core

layout (lines) in;
layout (triangle_strip, max_vertices = 4) out;

uniform vec3 screen_aspect = vec3(1.333, 1.0, 1.0);
uniform float line_size = 0.01;

in VertexData {
    vec2 texCoord;
    vec4 color;
    vec3 normal;
} vs[];

out VertexData {
    vec2 texCoord;
    vec4 color;
    vec3 normal;
} gs;

vec2 cross2d(vec2 v0) {
    return vec2(-1.0 * v0.y, v0.x);
}

vec3 screen_space(vec4 v)
{
    return vec3(v.xyz/v.w) * screen_aspect;
}

void main()
{
    vec3 p1 = screen_space(gl_in[0].gl_Position);
    vec3 p2 = screen_space(gl_in[1].gl_Position);

    vec3 n = normalize(vec3(cross2d(p2.xy - p1.xy), 0.0));
    vec3 offset = n * (line_size/2.0);

    gl_Position = vec4((p1 - offset)/screen_aspect, 1.0);
    gs.color = vs[0].color;
    EmitVertex();

    gl_Position = vec4((p1 + offset)/screen_aspect, 1.0);
    gs.color = vs[0].color;
    EmitVertex();

    gl_Position = vec4((p2 - offset)/screen_aspect, 1.0);
    gs.color = vs[1].color;
    EmitVertex();

    gl_Position = vec4((p2 + offset)/screen_aspect, 1.0);
    gs.color = vs[1].color;
    EmitVertex();

    EndPrimitive();
}