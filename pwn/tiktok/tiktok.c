//gcc tiktok.c -o tiktok -fstack-protector-all -Wl,-z,now,-z,relro -no-pie
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

#define NUM_SONGS 50

struct song{
    char song_path[24]; //24
    int fd;		//8
    char* album;	//8
    char* song;		//8
    char* contents;	//8
};//56

int song_count;
struct song songs[NUM_SONGS];

void list_options(){
    system("ls -R");
    printf("\nWhich song would you like to import?\n");
    printf("Please provide the entire file path.\n");
}

void import_song(){
    list_options();
    int nread = read(0, songs[song_count].song_path, sizeof(songs[song_count].song_path));
    if(nread <= 0){
        printf("Error reading input, exiting\n");
        exit(-1);
    }
    if(songs[song_count].song_path[nread-1] == '\n'){
        songs[song_count].song_path[nread-1] = '\x00';
    }
    songs[song_count].fd = open(songs[song_count].song_path, O_RDONLY);
    if(songs[song_count].fd == -1 || songs[song_count].song_path[0] < 'A' || songs[song_count].song_path[0] > 'Z' ||
        strstr(songs[song_count].song_path, "flag") || strstr(songs[song_count].song_path, "..")){
        printf("Error: Bad filepath, exiting\n");
        exit(-1);
    }
    songs[song_count].album = strtok(songs[song_count].song_path, "/");
    songs[song_count].song = strtok(NULL, ".");
}

void list_playlist(){
    for(int i = 0; i < song_count; i++){
        if (songs[i].album)
            printf("%d. %s-%s\n", i+1, songs[i].album, songs[i].song);
    }
}

void play_song(){
    int choice = 0;
    char length[5] = {0};
    unsigned int file_len = 0;
    printf("Which song would you like to play?\n");
    list_playlist();
    printf("Choice: ");
    scanf("%d", &choice);
    while ((getchar()) != '\n');
    choice--;
    if(choice >= song_count || choice < 0 || !songs[choice].album){
        printf("Error: Invalid Song Selection");
        return;
    }
    printf("You Selected: %s from %s\n", songs[choice].song, songs[choice].album);
    if (!songs[choice].contents){
        for(int i = 0; i < sizeof(length); i++){
            read(songs[choice].fd, length+i, 1);
            if(length[i] == '\n'){
                length[i] = '\x00';
                break;
            }
        }
        file_len = atoi(length);
        songs[choice].contents = malloc(file_len + 1);
        memset(songs[choice].contents, 0, file_len+1);
        read(songs[choice].fd, songs[choice].contents, file_len);
    }
    printf("%s", songs[choice].contents);
}

void remove_song(){
    int choice = 0;
    printf("Which song would you like to remove?\n");
    list_playlist();
    printf("Choice: ");
    scanf("%d", &choice);
    while ((getchar()) != '\n');
    choice--;
    if (choice < 0 || choice >= song_count || !songs[choice].album){
        printf("Error: Invalid Song Selection");
        return;
    }
    printf("Removing: %s from %s\n", songs[choice].song, songs[choice].album);
    songs[choice].song = 0;
    songs[choice].album = 0;
    free(songs[choice].contents);
    songs[choice].contents = 0;
    memset(songs[choice].song_path, 0, sizeof(songs[choice].song_path));
    close(songs[choice].fd);
    songs[choice].fd = 0;
}

void play_music(){
    while(1){
        int choice = 0;
        printf("\nSo what would you like to do today?\n");
        printf("1. Import a Song to the Playlist\n");
        printf("2. Show Playlist\n");
        printf("3. Play a song from the Playlist\n");
        printf("4. Remove a song from the Playlist\n");
        printf("5. Exit\n");
        printf("Choice: ");
        scanf("%d", &choice);
        while ((getchar()) != '\n');
        printf("\n");
        switch(choice){
            case 1:
                if(song_count >= NUM_SONGS){
                    printf("Error: Unable to Import Song, Library Full\n");
                }else{
                    import_song();
                    song_count++;
                }
                break;
            case 2:
                if(song_count > 0){
                    list_playlist();
                }else{
                    printf("Playlist is empty\n");
                }
                break;
            case 3:
                if(song_count > 0){
                    play_song();
                }else{
                    printf("Playlist is empty\n");
                }
                break;
            case 4:
                if (song_count > 0){
                    remove_song();
                }else{
                    printf("Playlist is empty\n");
                }
                break;
            case 5:
                printf("We're sad to see you go!\n");
                exit(0);
                break;
        }
    }
}

void welcome(){
    printf("Welcome to my tik tok rock bot!\n");
    printf("I really like Ke$ha, can you help me make a playlist?\n");
}

int main(){
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    welcome();
    play_music();
    return 0;
}
