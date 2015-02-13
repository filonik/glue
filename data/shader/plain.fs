#version 440 core

in VertexData {
    vec4 color;
    vec2 texCoord;
    vec3 normal;
} vs;

out vec4 fragColor;

void main() {
    fragColor = vs.color;
}