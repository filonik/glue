#version 440 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec4 color;
layout(location = 2) in vec2 texCoord;
layout(location = 3) in vec3 normal;

uniform mat4 projection;
uniform mat4 model_view;

out VertexData {
    vec4 color;
    vec2 texCoord;
    vec3 normal;
} vs;

void main() {
    gl_Position = projection * model_view * vec4(position, 1.0);
    
    vs.color = color;
    vs.texCoord = texCoord;
    vs.normal = normal;
}