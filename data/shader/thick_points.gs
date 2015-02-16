#version 400 core

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 projection;
uniform mat4 model_view;

uniform vec2 screen_aspect = vec2(1.333, 1.0);
uniform vec2 point_size = vec2(0.01);

vec2 screen_space(vec4 v)
{
    return vec2(v.xy/v.w) * screen_aspect;
}
void main()
{
    vec2 offset = point_size/2.0;
    
    for(int i = 0; i < gl_in.length(); i++)
    {
        vec2 position = screen_space(gl_in[i].gl_Position);
        
        gl_Position = vec4(vec2(position.x + offset.x, position.y + offset.y)/screen_aspect, 0.0, 1.0);
        //gs.normal = vec3(1.0, 0.0, 0.0);
        //gs.texCoord = vec2(1.0, 1.0);
        //gs.color = vs[i].color;
        EmitVertex();
        
        gl_Position = vec4(vec2(position.x + offset.x, position.y - offset.y)/screen_aspect, 0.0, 1.0);
        //gs.normal = vec3(1.0, 0.0, 0.0);
        //gs.texCoord = vec2(1.0, 0.0);
        //gs.color = vs[i].color;
        EmitVertex();
        
        gl_Position = vec4(vec2(position.x - offset.x, position.y + offset.y)/screen_aspect, 0.0, 1.0);
        //gs.normal = vec3(1.0, 0.0, 0.0);
        //gs.texCoord = vec2(0.0, 1.0);
        //gs.color = vs[i].color;
        EmitVertex();
        
        gl_Position = vec4(vec2(position.x - offset.x, position.y - offset.y)/screen_aspect, 0.0, 1.0);
        //gs.normal = vec3(1.0, 0.0, 0.0);
        //gs.texCoord = vec2(0.0, 0.0);
        //gs.color = vs[i].color;
        EmitVertex();
        
        EndPrimitive();
    }
}