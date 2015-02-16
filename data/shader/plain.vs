#version 440 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoord;
layout(location = 2) in vec4 color;
layout(location = 3) in vec3 normal;

uniform mat4 model_view_projection;

out VertexData {
    vec2 texCoord;
    vec4 color;
    vec3 normal;
} vs;

void main() {
    gl_Position = model_view_projection * vec4(position, 1.0);
    
    vs.texCoord = texCoord;
    vs.color = color;
    vs.normal = normal;
}