#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <raylib.h>


#define WIN_WIDTH 800
#define WIN_HEIGHT 600


typedef struct {
    Texture2D template;
    uint16_t x;
} Segment;


int main(void) {
    /*
     * init window
     */
    InitWindow(WIN_WIDTH, WIN_HEIGHT, "Dino");
    SetTargetFPS(60);

    /*
     * load graphics
     */
    Segment road = {
        .template = LoadTexture("graphics/road_template.png")
    };
 
    Segment cloud = {
        .template = LoadTexture("graphics/cloud_template.png")
    };

    /*
     * game loop
     */
    while(!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(WHITE);

        DrawTexturePro(
                road.template
                , (Rectangle) {road.x, 0, road.template.width, road.template.height}
                , (Rectangle) {40, WIN_HEIGHT/3*2, WIN_WIDTH-80, road.template.height}
                , (Vector2) {0, 0}, 0, WHITE);

        road.x = (road.x + 5) % road.template.width;

        DrawTexturePro(
                cloud.template
                , (Rectangle) {cloud.x, 0, cloud.template.width, cloud.template.height}
                , (Rectangle) {40, WIN_HEIGHT/3, WIN_WIDTH-80, cloud.template.height}
                , (Vector2) {0, 0}, 0, WHITE);

        cloud.x = (cloud.x + 1) % cloud.template.width;


        DrawFPS(10, 10);
        EndDrawing();
    }

    /*
     * clear recources
     */
    UnloadTexture(road.template);
    UnloadTexture(cloud.template);
    CloseWindow();
    
    return EXIT_SUCCESS;
}

