def mapper_entity(data):
    return {
        "id": data.id,
        "entityName": data.entityName,
        "location": mapper_country(data),
        "type": data.type,
        "creationDate": data.creationDate 
    }

def mapper_country(data):
    return {
        "id": data.locationId,
        "countryName": data.country.name,
        "alpha2Code": data.country.alpha2Code,
        "alpha3Code": data.country.alpha3Code,
    }


def mapper_position(data):
    return {
        "id": data.id,
        "positionName": data.positionName,
        "entity": {
            "id": data.entity.id,
            "entityName": data.entity.entityName
        }
         
    }

def mapper_nps(data):
    mapped_data = {
        "id": data.id,
        "score": data.score,
        "position": {
            "id": data.position.id,
            "positionName": data.position.positionName,
            "entityId": data.position.entityId
        }
    }

    if hasattr(data, 'user') and data.user:
        mapped_data["user"] = {
            "id": data.user.id,
            "userName": data.user.userName,
            "email": data.user.email
        }

    return mapped_data
