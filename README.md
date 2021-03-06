# glue
Python OpenGL Utilities and Extensions.

## Basic Usage

The library aims to aid rapid prototyping with OpenGL. It is under development and subject to change. Currently, it can be used as follows:

In `plain_texture.vs`:

```glsl
#version 440 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoord;
layout(location = 2) in vec4 color;
layout(location = 3) in vec3 normal;

uniform mat4 projection;
uniform mat4 model_view;

out VertexData {
    vec2 texCoord;
    vec4 color;
    vec3 normal;
} vs;

void main() {
    gl_Position = projection * model_view * vec4(position, 1.0);
    
    vs.texCoord = texCoord;
    vs.color = color;
    vs.normal = normal;
}
```

In `plain_texture.fs`:

```glsl
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
```

In `main.py`:

```python
program = None
texture = None
vao = None
vbo = None

def rect(w=1.0, h=1.0):
    data = np.zeros(4, dtype = [
        ("position", np.float32, 3),
        ("texCoord", np.float32, 2),
        ("color", np.float32, 4),
        ("normal", np.float32, 3),
    ])
    
    w_half, h_half = w/2.0, h/2.0
    
    data['position'] = [(-w_half, -h_half, 0), (-w_half, +h_half, 0), (+w_half, -h_half, 0), (+w_half, +h_half, 0)]
    data['texCoord'] = [(0, 0), (0, +1), (+1, 0), (+1, +1)]
    data['color'] = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)]
    data['normal'] = [(+1, 0, 0), (+1, 0, 0), (+1, 0, 0), (+1, 0, 0)]
    
    return data

def init(window):
    global program, texture, vao, vbo
    
    program = gl.utilities.load_program([
        'data/shader/plain_texture.vs',
        'data/shader/plain_texture.fs',
    ])
    
    texture = gl.utilities.load_texture('data/image/smile.png')
    
    vao = gl.VertexArrayObject()
    gl.VertexArrayObject.bind(vao)
    
    vbo = gl.VertexBufferObject()
    gl.VertexBufferObject.bind(vbo)
    vbo.set_data(rect())

def render(window):
    global program, texture, vao, vbo
    
    gl.clear_color([1.0,1.0,1.0])
    gl.clear()
    
    size = np.asarray(window.size)
    aspect = size / np.min(size)
    
    projection = projections.ortho(-aspect[0], +aspect[0], -aspect[1], +aspect[1], -1.0, +1.0)
    model_view = transforms.translate(0.0, np.sin(2*np.pi*(np.fmod(time.time(), 5.0)/5.0)), 0.0)
    
    gl.Program.bind(program)
    
    program.uniforms['projection'] = projection
    program.uniforms['model_view'] = model_view
    program.uniforms['texture'] = texture
    
    program.inputs['position'] = vbo
    program.inputs['texCoord'] = vbo
    program.inputs['color'] = vbo
    program.inputs['normal'] = vbo
    
    GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 4)

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