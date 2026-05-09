import struct
import pygame
import moderngl
import numpy as np
import pygame.surfarray


VERTEX_SHADER = """
#version 300 es
in vec2 vert;
in vec2 in_text;
out vec2 v_text;
void main() {
   gl_Position = vec4(vert, 0.0, 1.0);
   v_text = in_text;
}
"""

FRAGMENT_SHADER = """
#version 300 es
precision mediump float;
uniform sampler2D Texture;
out vec4 color;
in vec2 v_text;
uniform int mode;
void main() {
  if (mode == 0){
    color = vec4(texture(Texture, v_text).rgb, 1.0);
  }
  else{
    float flatness = 1.0;
    if (mode == 1)flatness = 2.7;
    else if(mode == 2)flatness = 10.0;
    vec2 center = vec2(0.5, 0.5);
    vec2 off_center = v_text - center;

    off_center *= 1.0 + 0.8 * pow(abs(off_center.yx), vec2(flatness));
    vec2 v_text2 = center+off_center;

    if (v_text2.x > 1.0 || v_text2.x < 0.0 ||
        v_text2.y > 1.0 || v_text2.y < 0.0){
      color=vec4(0.0, 0.0, 0.0, 1.0);
    } else {
      color = vec4(texture(Texture, v_text2).rgb, 1.0);
      float fv = fract(v_text2.y * float(textureSize(Texture,0).y));
      fv=min(1.0, 0.8+0.5*min(fv, 1.0-fv));
      color.rgb*=fv;
    }
  }
}
"""

class ShaderEngine:
    def __init__(self, width, height, style=1):
        self.width = width
        self.height = height
        self.style = style
        
        self.ctx = moderngl.create_context()
        
        # Full-screen quad coordinates
        self.texture_coordinates = np.array([
            0.0, 0.0,  1.0, 0.0,
            0.0, 1.0,  1.0, 1.0
        ], dtype='f4')
        self.world_coordinates = np.array([
            -1.0, -1.0,  1.0, -1.0,
            -1.0,  1.0,  1.0,  1.0
        ], dtype='f4')
        self.render_indices = np.array([
            0, 1, 2,
            1, 2, 3
        ], dtype='i4')
        
        self.prog = self.ctx.program(
            vertex_shader=VERTEX_SHADER,
            fragment_shader=FRAGMENT_SHADER,
        )
        self.prog['mode'] = self.style
        
        self.vbo = self.ctx.buffer(self.world_coordinates)
        self.uvmap = self.ctx.buffer(self.texture_coordinates)
        self.ibo = self.ctx.buffer(self.render_indices)
        
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vbo, '2f', 'vert'),
                (self.uvmap, '2f', 'in_text'),
            ],
            index_buffer=self.ibo
        )
        
        # Use 3 components (RGB). 1000 * 3 is a multiple of 4, so alignment should be fine.
        self.texture = self.ctx.texture((width, height), 3)







    def render(self, surface):
        # 1. Capture the surface as RGB (width, height, 3)
        # array3d is generally the most reliable way to get pixels from a surface
        img = pygame.surfarray.array3d(surface)
        
        # 2. Transpose from (width, height, 3) to (height, width, 3)
        img = np.transpose(img, (1, 0, 2))
        
        # 3. Flip vertically to align with OpenGL's bottom-up coordinate system
        img = np.flipud(img)
        
        # 4. Convert to contiguous bytes to avoid stride/alignment issues on Intel GPUs
        data = np.ascontiguousarray(img, dtype='u1').tobytes()
        
        # 5. Upload and Render
        self.texture.write(data)
        self.ctx.clear(0, 0, 0, 1)
        self.texture.use()
        self.vao.render()



        # 2. Clear the OpenGL context
        self.ctx.clear(0, 0, 0, 1)

        # 3. Use the texture and render the quad
        self.texture.use()
        self.vao.render()
