#version 460 core

uniform sampler2D texture1;
varying vec2 v_texture_coordinates;

void main() {

    gl_FragColor = texture2D(texture1, v_texture_coordinates);
}