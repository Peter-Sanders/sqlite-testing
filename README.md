need to have docker installed on your machine, maybe docker desktop as well
easiest path is to just install docker desktop


run this command 

docker buildx build . 



this will build a docker image called 'sqlite-testing'


then run 

docker run -it sqlite-testing 


this will run the container and open a shell into it in the current terminal


then just run  

python main.py 


then you can CTRL D to exit the container 
