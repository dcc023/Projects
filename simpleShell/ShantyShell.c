#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

//Built-in commands:
int sscd(char **args);
int ssinfo(char **args);
int sspwd(char **args);
int ssexit(char **args);

//List of builtin commands:
char *builtins[] =
{
  "cd", "info", "pwd", "exit"
};

//Builtin functions array:
int(*builtinfuncs[]) (char **) =
{
  &sscd, &ssinfo, &sspwd, &ssexit
};

int totalbuiltins()
{
  return sizeof(builtins) / sizeof(char *);
}

//Builtin functionality:
int sscd(char **args)  //for the cd command
{
  if(args[1] == NULL)  //if there is no second token, then there was no input after cd, so it shouldnt work
  {
    fprintf(stderr, "You cannot change directory to nothingness, idiot.. \n");
  }
  else
  {
    if(chdir(args[1]) != 0)  //will run chdir and also check if it gets an error
    {
      perror("error");
    }
  }
  return 1;
}

int ssinfo(char **args)
{
  printf("Welcome to the Shanty Shell by Dylan Campbell\n");
  printf("This program works almost exactly like the normal Unix shell! \n");
  printf(" BUT WITH WAY LESS FUNCTIONALITY! \n \n");
  printf(" All of the builtin commands we got here are cd, pwd, exit, and well.. info. \n");
  printf("We've also ripped off all the non-builtins, so you can just use man and search whatever. \n");
  return 1;
}

int sspwd(char **args)
{
  char cwd[1024];

  if(getcwd(cwd, sizeof(cwd)) != 0)
  {
    perror("getcwd error");
  }
  else
  {
    printf("Current directory is %s \n", cwd);
  }
}

int ssexit(char **args)
{
  return 0;
}

//END OF BUILTINS

int execute(char **args)
{
  int i;

  if(args[0] == NULL)
  {
    return 1;
  }
  
  for(i = 0; i < totalbuiltins(); i++)
  {
    if(strcmp(args[0], builtins[i]) == 0)
    {
      return(*builtinfuncs[i])(args);
    }
  }
  return givebirth(args);
}


int givebirth(char **args)  //Used to fork a process
{
  pid_t pid, wpid;
  int status;

  pid = fork();  //creates the child process
  if(pid == 0)   //If the PID is 0, then it must be the child process
  {
    if(execvp(args[0], args) == -1) //this will run execvp, while also wanting to check the return, we shouldnt get -1 unless bad things
    {
      perror("error child");
    } 
    exit(EXIT_FAILURE);  //exit so shell can keep running
  }
  else if(pid < 0)  //in case of an error with the fork itself
  {
    perror("error fork");
  }
  else  //This means the process was successful and should return its PID to the parent
  {
    do
    {
      wpid = waitpid(pid, &status, WUNTRACED);
    }while(!WIFEXITED(status) && !WIFSIGNALED(status));  //We wait until process is exited or killed
  }
  
  return 1;
}

#define tokenbufsize 64
char **tokenline(char *line)
{
  int bufsize = tokenbufsize;  
  int position = 0;
  char **tokens = malloc(bufsize * sizeof(char*));
  char *token;
  

  if(!tokens)  //if there are no tokens, we bail
  {
    fprintf(stderr, "Could not allocate \n");
    exit(EXIT_FAILURE);
  }

  token = strtok(line, " \t\r\n\a");  //this will define a token, gathering chars for a string until it hits our defined delimeters
  while(token != NULL)
  {
    tokens[position] = token;  //assign the just defined token to the tokens array for later use
    position++;  //increment the position in the array

    if(position >=bufsize)  //just in case we use more than our bufsize has defined, we increase it
    {
      bufsize += tokenbufsize;
      tokens = realloc(tokens, bufsize * sizeof(char*));
      if(!tokens)
      {
        fprintf(stderr, "Could not allocate \n");
        exit(EXIT_FAILURE);
      }
    }
    
    token = strtok(NULL, " \t\r\n\a");
  }
  tokens[position] = NULL;  //making sure the last spot in the array is NULL for executing.
  return tokens;  //We are now going to return the array of tokens we have created.
}

#define realbufsize 1024
char *readline(void)
{
  int bufsize = realbufsize;
  int position = 0;
  char *buffer = malloc(sizeof(char) * bufsize);
  int c;

  if(!buffer)
  {
    fprintf(stderr, "Could not allocate memory \n");
    exit(EXIT_FAILURE);  
  }

  while(1)
  {
    c = getchar();  //This will read a character

    if( c == EOF || c == '\n')  //We will check if the character is at EOF or a line break
    {
      buffer[position] = '\0';  //If so, we will put a null character there, for our tokenizer later
      return buffer;
    }
    else
    {
      buffer[position] = c;    //Saves the character to the buffer array
    }
    position++;  //Will move on to next slot of the array
    
    if(position >= bufsize)  //Just in case our position exceeds our currently defined buffer size, we redefine the bufsize larger
    {
      bufsize += realbufsize;
      buffer = realloc(buffer, bufsize);
      if(!buffer)
      {
        fprintf(stderr, "Could not allocate \n");
        exit(EXIT_FAILURE);
      }
    }
  }
}

void shloop(void)
{
  char *line;
  char **args;
  int status;

  do
  {
    printf("~ ");
    line = readline(); //this is gonna read the line and apply buffers
    args = tokenline(line); //We can utilize the buffers we created to then tokenize the input
    status = execute(args); //Now we can execute the input using the tokens

    free(line);
    free(args);
  } while(status);
}

int main(int argc, char **argv)
{
  printf("Welcome to the Shanty Shell!\n");
  printf("Type info for more info \n");
  shloop();

  return EXIT_SUCCESS;
}
