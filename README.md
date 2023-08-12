# App Notes

### MySQL

- Run SQL script from file: `mysql -u root < init.sql`
- Drop database: mysql -u root -e "DROP DATABASE auth"
- Drop user: mysql -u root -e "DROP user johndoe@localhost"

### Kubernetes

- Apply: kubectl apply -f <folder|file_name>
- Scale down: kubectl scale deployment --replicas=0 <deployment_name>
