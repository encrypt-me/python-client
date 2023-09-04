# Encrypt Me Client

## Installation

### MacOS
You can use bash script from this repo
```
$ git clone https://github.com/encrypt-me/python-client.git
$ cd python-client
$ chmod +x encrypt-me
$ ./encrypt-me --help
```

## Usage
To encrypt a message with an user "support@encrypt-me.org" public key 
```
$ encrypt-me -e support@encrypt-me.org --message "Hello World"
```

It will provide the output

```
-----ENCRYPTED WITH ENCRYPT-ME.ORG-----
BAHJgXVYyd90YNIHUl/qNaIpDWIuCotO/TbCcdNNemTvJj8kDIoS74j6wmCznLia
szXscBnqb0fFBenFh7mS3z7+SQDt6zUjGMX0Hnfj93s5es4QN/RnHZtyTSh1vSCS
I3GfqzjPvQRZTy82wGFWOJkcTnfPb5DT6egQ1+JmHowkR7QdoQJJXtHU92e/k7dt
N0ci2j4JeQgBlQ/uIBYZyQ==
-----ENCRYPTED WITH ENCRYPT-ME.ORG-----
```

To decrypt a message with your private key
```
$ encrypt-me --decrypt
Enter encrypted data:
-----ENCRYPTED WITH ENCRYPT-ME.ORG-----
BAHJgXVYyd90YNIHUl/qNaIpDWIuCotO/TbCcdNNemTvJj8kDIoS74j6wmCznLia
szXscBnqb0fFBenFh7mS3z7+SQDt6zUjGMX0Hnfj93s5es4QN/RnHZtyTSh1vSCS
I3GfqzjPvQRZTy82wGFWOJkcTnfPb5DT6egQ1+JmHowkR7QdoQJJXtHU92e/k7dt
N0ci2j4JeQgBlQ/uIBYZyQ==
-----ENCRYPTED WITH ENCRYPT-ME.ORG-----


-----BEGIN DECRYPTED MESSAGE-----
Hello World
-----END DECRYPTED MESSAGE-----
```

It will ask you to paste the encrypted message

## Public Key Registration 
To register your public key, you can use the following command
```
$ encrypt-me --register support@encrypt-me.org
```

It will ask you to paste encrypted validation message which sent to a given email address.

