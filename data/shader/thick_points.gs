#version 400 core

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform vec3 screen_aspect = vec3(1.333, 1.0, 1.0);
uniform vec2 point_size = vec2(0.01);

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

vec3 screen_space(vec4 v)
{
    return vec3(v.xyz/v.w) * screen_aspect;
}

void main()
{
    vec2 offset = point_size/2.0;
    
    for(int i = 0; i < gl_in.length(); i++)
    {
        vec3 position = screen_space(gl_in[i].gl_Position);
        
        gl_Position = vec4(vec3(position.x + offset.x, position.y + offset.y, position.z)/screen_aspect, 1.0);
        //gs.normal = vec3(1.0, 0.0, 0.0);
        //gs.texCoord = vec2(1.0, 1.0);
        gs.color = vs[i].color;
        EmitVertex();
        
        gl_Position = vec4(vec3(position.x + offset.x, position.y - offset.y, position.z)/screen_aspect, 1.0);
        //gs.normal = vec3(1.0, 0.0, 0.0);
        //gs.texCoord = vec2(1.0, 0.0);
        gs.color = vs[i].color;
        EmitVertex();
        
        gl_Position = vec4(vec3(position.x - offset.x, position.y + offset.y, position.z)/screen_aspect, 1.0);
        //gs.normal = vec3(1.0, 0.0, 0.0);
        //gs.texCoord = vec2(0.0, 1.0);
        gs.color = vs[i].color;
        EmitVertex();
        
        gl_Position = vec4(vec3(position.x - offset.x, position.y - offset.y, position.z)/screen_aspect, 1.0);
        //gs.normal = vec3(1.0, 0.0, 0.0);
        //gs.texCoord = vec2(0.0, 0.0);
        gs.color = vs[i].color;
        EmitVertex();
        
        EndPrimitive();
    }
}