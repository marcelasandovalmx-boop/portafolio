import json, re
W = json.load(open('../1-corte/words.json'))
norm = lambda s: re.sub(r'[^\wáéíóúñü]', '', s.lower())
# (cerca de, palabra clave)  — una por frase
K = [(0.0,'polémico'),(6.3,'acuerdo'),(10.3,'conclusión'),(16,'recomiende'),(19.3,'repito'),(21.1,'mundo'),
 (24.1,'contraproducente'),(28.1,'conocen'),(34,'feliz'),(40.2,'términos'),(44.9,'recomendar'),(48.9,'hago'),
 (49.7,'peligroso'),(58.5,'precio'),(61.1,'concesiones'),(64.7,'urgencia'),(67.5,'más'),(70,'venga'),(73,'ceder'),
 (80.1,'detente'),(81.5,'cliente'),(86.8,'barato'),(94.7,'regateó'),(97,'deshoras'),(100.4,'recomiende'),(102,'decir'),
 (104.9,'superbarato'),(110,'ordenado'),(114.2,'gratis'),(115,'más'),(117.2,'contraproducente'),(122.3,'respetan'),
 (127.6,'similares'),(131,'regateando'),(136.8,'negocio'),(139,'paso'),(142.2,'cotización'),(145,'presupuesto'),
 (150,'último'),(156,'personalidad'),(160,'peligroso'),(166,'costaba'),(173.6,'clientes'),(177.3,'ellos'),
 (180.3,'comentarios'),(182.3,'correcta'),(190.1,'sea'),(193.9,'clientes'),(196.3,'respeten'),(199,'advertí')]
out = []
for near, k in K:
    c = [i for i, w in enumerate(W) if norm(w['word']) == norm(k) and w['start'] >= near - 0.5]
    i = min(c, key=lambda i: W[i]['start'] - near)
    out.append({'i': i, 'palabra': W[i]['word'], 'clave': k, 'start': W[i]['start'], 'end': W[i]['end']})
json.dump(out, open('claves.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), 'claves')
