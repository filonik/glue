#version 400 core

layout (lines) in;
layout (triangle_strip, max_vertices = 4) out;

uniform vec2 screen_aspect = vec2(1.333, 1.0);
uniform float line_size = 0.01;

vec2 cross2d(vec2 v0) {
    return vec2(-1.0 * v0.y, v0.x);
}

vec2 screen_space(vec4 v)
{
    return vec2(v.xy/v.w) * screen_aspect;
}

void main()
{
    vec2 p1 = screen_space(gl_in[0].gl_Position);
    vec2 p2 = screen_space(gl_in[1].gl_Position);

    vec2 n = normalize(cross2d(p2.xy - p1.xy));
    vec2 offset = n * (line_size/2.0);

    gl_Position = vec4((p1 - offset)/screen_aspect, 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4((p1 + offset)/screen_aspect, 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4((p2 - offset)/screen_aspect, 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4((p2 + offset)/screen_aspect, 0.0, 1.0);
    EmitVertex();

    EndPrimitive();
}