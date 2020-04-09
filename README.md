# PyJudger


<img src="https://i.redd.it/pn6uv9w5f0q31.png" width="80%">

##

Falcon based REST API that main function is to analyze quality of face on given image. 



### Run Locally 

PyJudger is docker based service, therefore all you got to do is build docker image and run docker-compose


```
Build docker:  
$ docker-compose build

Start server :
$ docker-compose up
```

by default it is running on *0.0.0.0:8313*


### Black 
Project is formatted with *[Black](https://pypi.org/project/black/ "pypi")*  

```
docker-compose run core sh -c "black core/*"
```





## Available Endpoints 

Sample body can be found in _code/tests/filter_input.json_

To generalize usage body requires only one attribute 

```buildoutcfg
{
  url: "www.someimagehosting.com/faceimage.jpg"
}
```

Sample images I have no rights to: 

Blurry: https://i.ibb.co/b6GhhKL/blurry.jpg

Sharp: https://i.ibb.co/QY7zRjz/sharp.jpg




> [http POST] /filter/all
```

    {  
      "var_laplacian": 52.40,
      "is_frontal": "FRONTAL",
    }
```


> [http POST] /filter/isFrontal
```
    {
      "is_frontal": "FRONTAL"
    }
```

> [http POST] /filter/laplacian
```
    {
      "var_laplacian": 800.01
    }
 ```
 > [http GET] /health
```   
    {
     "message": "OK"
    }    
```


##TODO

[ ] Measure distance between eyes for better sharpness scaling

[ ] Allow thresholds to be passed in body

[ ] Divide image into smaller-blocks for better sharpness analysis 

[ ] Logger 

[ ] More tests! 
