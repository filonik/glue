# glue
Python OpenGL Utilities and Extensions.

## Basic Usage

The library aims to allow rapid prototyping with OpenGL. It is under development and subject to change. Currently, it can be used as follows:

In `plain.vs`:

```c
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
```

In `plain.fs`:

```c
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
```

In `main.py`:

```python
program = None
vao = None
vbo = None

def init(window):
    global program, vao, vbo
    
    program = utilities.load_program([
        'data/shader/plain.vs',
        'data/shader/plain.fs',
    ])
    
    vao = gl.VertexArrayObject()
    gl.VertexArrayObject.bind(vao)
    
    vbo = gl.VertexBufferObject()
    gl.VertexBufferObject.bind(vbo)
    vbo.set_data(rect())

def render(window):
    global program, vao, vbo
    
    gl.clear_color([1.0,1.0,1.0])
    gl.clear()
    
    gl.Program.bind(program)
    
    size = np.asarray(window.size)
    aspect = size / np.min(size)
    
    projection = projections.ortho(-aspect[0], +aspect[0], -aspect[1], +aspect[1], -1.0, +1.0)
    model_view = transforms.translate(0, np.sin(2*np.pi*np.fmod(time.time(), 5.0)/5.0), 0)
    
    program.uniforms['projection'] = projection
    program.uniforms['model_view'] = model_view
    
    program.attributes['position'] = vbo
    program.attributes['color'] = vbo
    
    GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, vbo.type.dtype['position'].size)

def main():
    window = glfw.Window((800, 600), "Hello GLUE!")
    glfw.Context.set_current(window.context)
    
    info()
    
    init(window)
    
    gl.cleanup()
    
    while not window.should_close():
        glfw.poll_events()
        
        render(window)
        
        gl.cleanup()
        
        window.swap_buffers()
    
    window.dispose()

if __name__ == "__main__":
    with glfw.initialized():
        main()
```

See `main.py` for complete code listing.