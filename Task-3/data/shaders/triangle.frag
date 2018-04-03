#version 430 core
in vec4 normalColor;

layout(location=0) out vec4 FragColor;

void main()
{
    FragColor = normalColor;
}