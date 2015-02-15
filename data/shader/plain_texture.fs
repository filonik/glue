#version 440 core

uniform sampler2D texture;

in VertexData {
    vec2 texCoord;
    vec4 color;
    vec3 normal;
} vs;

out vec4 fragColor;

void main() {
    fragColor = texture2D(texture, vs.texCoord);
}