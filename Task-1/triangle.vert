attribute vec4 vPosition;
attribute vec4 color;

out varying vec4 normalColor;

void main()
{
    gl_Position = vPosition;
    normalColor = color;
}