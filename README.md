# BlogWebsite

<i>This was part of my college lab work</i>

**The aim of this project was to create a web application to represent the use of database and the python programming.**

![Home page](https://github.com/dragoFireup/BlogWebsite/blob/master/home.png)

![Create post](https://github.com/dragoFireup/BlogWebsite/blob/master/add_post.png)
### Application details

<ul>
    <li>
        Backend:
        <ul>
            <li>
                Python: 3.6
            </li>
            <li>
                Django: 2.2
            </li>
        </ul>
    </li>
    <li>
        Frontend:
        <ul>
            <li>
                HTML5
            </li>
            <li>
                CSS3 (Bulma framework)
            </li>
            <li>
                JavaScript (ES6)
            </li>
        </ul>
    </li>
</ul>

### Models used

##### User
Used Django user authentication model

The parameters can be found at [Django's official site](https://docs.djangoproject.com/en/3.0/topics/auth/default/)

##### Profile
| Field | Type | Description |
| ----- | ---- | ----------- |
| user | ForeignKey | Linked to the User model | 
| email_confirmed | Boolean | Email confirmation value |

##### Blog
| Field | Type | Description |
| ----- | ---- | ----------- |
| author | ForeignKey | Linked to the User model |
| text | TextField | Text of the blog |
| created_date | DateField | Date the post was created |
| published_data | DateField | Date the post was published |
| image | ImageField | The url of the image of the post |

### How to use the site

- If you already have an account, login.
- If you don't have one you can create an account and will be allowed to login after email verification.
- You can view all the other posts of the user
- You can see your own posts too.