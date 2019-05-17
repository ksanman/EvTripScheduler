def ToJson(instance):
    return {k:v for k , v in vars(instance).items() if not str(k).startswith('_')}

from address_info import AddressInfo
from charger import Charger
from user import User
from connection import Connection
from user_comment import UserComment
from media_item import MediaItem
import json
import psycopg2 as db
import psycopg2.sql as sql
from psycopg2.extras import RealDictCursor

class ChargerContext:
    def __init__(self, host="localhost", dbname="evvehicle", user="evvehicle", password="ev-vehicle"):
        self.Host = host
        self.DbName = dbname
        self.User = user
        self.Password = password

    def Connect(self):
        connection = db.connect(host=self.Host, dbname=self.DbName, user=self.User, password=self.Password)
        connection.autocommit = True
        return connection

    def GetChargersFromJson(self, jsonData):
        """
        Gets the charger objects from the a charger request json file saved locally. 
        """
        chargers = []
        for data in jsonData:
            chargers.append(self.ObjectDecoder(data))
        return chargers

    def GetChargersFromFile(self, filePath):
        """
        Load the nearest chargers from a file. 
        """
        with open(filePath, 'r') as f:
            data = json.loads(f.read())

        return self.GetChargersFromJson(data)

    def AddressDecoder(self, addressInfo):
        """
        Function used to decode a json string into an AddressInfo object. 
        """
        return AddressInfo(addressInfo['AccessComments'] if 'AccessComments' in addressInfo else None,
            addressInfo['AddressLine1'] if 'AddressLine1' in addressInfo else None,
            addressInfo['AddressLine2'] if 'AddressLine2' in addressInfo else None,
            addressInfo['ContactEmail'] if 'ContactEmail' in addressInfo else None,
            addressInfo['ContactTelephone1'] if 'ContactTelephone1' in addressInfo else None,
            addressInfo['ContactTelephone2'] if 'ContactTelephone2' in addressInfo else None,
            addressInfo['CountryID'] if 'CountryID' in addressInfo else None,
            addressInfo['DistanceUnit'] if 'DistanceUnit' in addressInfo else None,
            addressInfo['ID'] if 'ID' in addressInfo else None,
            addressInfo['Latitude'] if 'Latitude' in addressInfo else None,
            addressInfo['Longitude'] if 'Longitude' in addressInfo else None,
            addressInfo['Postcode'] if 'Postcode' in addressInfo else None,
            addressInfo['RelatedUrl'] if 'RelatedUrl' in addressInfo else None,
            addressInfo['StateOrProvince'] if 'StateOrProvince' in addressInfo else None,
            addressInfo['Title'] if 'Title' in addressInfo else None,
            addressInfo['Town'] if 'Town' in addressInfo else None)

    def ObjectDecoder(self, obj):
        """
        Function used to decode a json string into a Charger object. 
        """
        if 'AddressInfo' in obj:
            addressInfo = obj['AddressInfo']
            a_info= self.AddressDecoder(addressInfo)

        if "Connections" in obj:
            connections = []
            for c in obj['Connections']:
                connections.append(Connection(
                    c["Amps"] if 'Amps' in c else None,
                    c["ConnectionTypeID"] if 'ConnectionTypeID' in c else None,
                    c["CurrentTypeID"] if 'CurrentTypeID' in c else None,
                    c["ID"] if 'ID' in c else None,
                    c["LevelID"] if 'LevelID' in c else None,
                    c["PowerKW"] if 'PowerKW' in c else None,
                    c["Quantity"] if 'Quantity' in c else None,
                    c["StatusTypeID"] if 'StatusTypeID' in c else None,
                    c["Voltage"] if 'Voltage' in c else None,
                ))

        mediaItems = []
        if "MediaItems" in obj:
            for m in obj["MediaItems"]:
                try:
                    mediaItems.append(MediaItem(
                        User(m["User"]["ID"],
                                m["User"]["ProfileImageURL"] if 'ProfileImageURL' in m['User'] else None,
                                m["User"]["ReputationPoints"] if 'ReputationPoints' in m['User'] else None,
                                m["User"]["Username"] if 'Username' in m['User'] else None
                        ) if 'User' in m else None,
                        m["ChargePointID"] if 'ChargePointID' in m else None,
                        m["Comment"] if 'Comments' in m else None,
                        m["DateCreated"] if 'DateCreated' in m else None,
                        m["ID"] if 'ID' in m else None,
                        m["IsEnabled"] if 'IsEnabled' in m else None,
                        m["IsExternalResource"] if 'IsExternalResource' in m else None,
                        m["IsFeaturedItem"] if 'IsFeaturedItem' in m else None,
                        m["IsVideo"] if 'IsVideo' in m else None,
                        m["ItemThumbnailURL"] if 'ItemThumbnailURL' in m else None,
                        m["ItemURL"] if 'ItemURL' in m else None
                    ))
                except Exception as e:
                    print('Media Item Exception: ', e)
                    print(m)
        userComments = []         
        if "UserComments" in obj:
            for u in obj["UserComments"]:
                try:
                    userComments.append(UserComment(
                        User(u["User"]["ID"],
                                u["User"]["ProfileImageURL"] if 'ProfileImageURL' in u['User'] else None,
                                u["User"]["ReputationPoints"] if 'ReputationPoints' in u['User'] else None,
                                u["User"]["Username"] if 'Username' in u['User'] else None
                        ) if 'User' in u else None,
                        u["ChargePointID"] if 'ChargePointID' in u else None,
                        u["CheckinStatusTypeID"] if 'CheckinStatusTypeID' in u else None,
                        u["CommentTypeID"] if 'CommentTypeID' in u else None,
                        u["DateCreated"] if 'DateCreated' in u else None,
                        u["ID"] if 'ID' in u else None,
                        u["Rating"] if 'Rating' in u else None,
                        u["UserName"] if 'UserName' in u else None
                    ))
                except Exception as e:
                    print('User Comment Exception: ', e)
                    print(u)

        charger = Charger(a_info, connections, mediaItems, userComments,
            obj["DataProviderID"] if 'DataProviderID' in obj else None,
            obj["DataQualityLevel"] if 'DataQualityLevel' in obj else None,
            obj["DateCreated"] if 'DateCreated' in obj else None,
            obj["DateLastStatusUpdate"] if 'DateLastStatusUpdate' in obj else None,
            obj["DateLastVerified"] if 'DateLastVerified' in obj else None,
            obj["GeneralComments"] if 'GeneralComments' in obj else None,
            obj["ID"] if 'ID' in obj else None,
            obj["IsRecentlyVerified"] if 'IsRecentlyVerified' in obj else None,
            obj["NumberOfPoints"] if 'NumberOfPoints' in obj else None,
            obj["OperatorID"] if 'OperatorID' in obj else None,
            obj["StatusTypeID"] if 'StatusTypeID' in obj else None,
            obj["SubmissionStatusTypeID"] if 'SubmissionStatusTypeID' in obj else None,
            obj["UUID"] if 'UUID' in obj else None,
            obj["UsageCost"] if 'UsageCost' in obj else None,
            obj["UsageTypeID"] if 'UsageTypeID' in obj else None,
            obj["IntersectionLatitude"] if "IntersectionLatitude" in obj else None,
            obj["IntersectionLongitude"] if "IntersectionLongitude" in obj else None
            )

        return charger

    def createDatabase(self):
        conn = self.Connect()
        # create a cursor object called cur
        cur = conn.cursor()
                
        # construct a query string
        strSql = """
        --DO
        --$do$
        --BEGIN
            CREATE EXTENSION IF NOT EXISTS postgis; -- enable extension 
            
            CREATE TABLE IF NOT EXISTS ev.AddressInfo
            (
                ID INTEGER NOT NULL PRIMARY KEY,
                AccessComments VARCHAR(5000),
                AddressLine1 VARCHAR(200),
                AddressLine2 VARCHAR(200),
                ContactEmail VARCHAR(500),
                ContactTelephone1 VARCHAR(50),
                ContactTelephone2 VARCHAR(50),
                CountryID INTEGER,
                DistanceUnit INTEGER,
                Latitude FLOAT,
                Longitude FLOAT,
                Postcode VARCHAR(50),
                RelatedURL VARCHAR(500),
                StateOrProvince VARCHAR(100),
                Title VARCHAR(500),
                Town VARCHAR(500),
                Location GEOGRAPHY(Point, 4326)
            );

            CREATE INDEX geo_spx ON ev.AddressInfo USING GIST (Location);
        --END
        --$do$

        --DO 
        --$do$
        --BEGIN
            CREATE TABLE IF NOT EXISTS ev.Charger(
                ID INTEGER NOT NULL PRIMARY KEY,
                AddressInfoID INTEGER NOT NULL REFERENCES ev.AddressInfo(ID),
                DataProviderID INTEGER,
                DataQualityLevel INTEGER,
                DateCreated VARCHAR(50),
                DateLastStatusUpdate VARCHAR(50),
                DateLastVerified VARCHAR(50),
                GeneralComments VARCHAR(1000),
                IsRecentlyVerified BOOLEAN,
                NumberOfPoints INTEGER,
                OperatorID INTEGER,
                StatusTypeID INTEGER,
                SubmissionStatusTypeID INTEGER,
                UUID VARCHAR(200),
                UsageCost VARCHAR(500),
                UsageTypeID INTEGER
            );
        --END
        --$do$

        --DO 
        --$do$
        --BEGIN
            CREATE TABLE IF NOT EXISTS ev.Connection
            (
                ID INTEGER NOT NULL PRIMARY KEY,
                ChargerID INTEGER NOT NULL REFERENCES ev.Charger(ID),
                Amps INTEGER,
                ConnectionTypeID INTEGER,
                CurrentTypeID INTEGER,
                LevelID INTEGER,
                PowerKw FLOAT,
                Quantity INTEGER,
                StatusTypeID INTEGER,
                Voltage INTEGER
            );
        --END
        --$do$

        --DO 
        --$do$
        --BEGIN
            CREATE TABLE IF NOT EXISTS ev.OcmUser
            (
                ID INT NOT NULL PRIMARY KEY,
                ProfileImageURL VARCHAR(500),
                ReputationPoints INTEGER,
                Username VARCHAR(200)
            );
        --END
        --$do$

        --DO 
        --$do$
        --BEGIN
            CREATE TABLE IF NOT EXISTS ev.MediaItem
            (
                ID INTEGER NOT NULL PRIMARY KEY,
                ChargePointID INTEGER NOT NULL REFERENCES ev.Charger(ID),
                Comment VARCHAR(500),
                DateCreated VARCHAR(50),
                IsEnabled BOOLEAN,
                IsExternalResource BOOLEAN,
                IsFeaturedItem BOOLEAN,
                IsVideo BOOLEAN,
                ItemThumbnailURL VARCHAR(500),
                ItemURL VARCHAR(500),
                UserID INTEGER REFERENCES ev.OcmUser(ID)
            );
        --END
        --$do$

        --DO 
        --$do$
        --BEGIN
            CREATE TABLE IF NOT EXISTS ev.UserComment
            (
                ID INTEGER NOT NULL PRIMARY KEY,
                ChargePointID INTEGER,
                CheckinStatusTypeID INTEGER,
                CommentTypeID INTEGER,
                DateCreated VARCHAR(50),
                Rating INTEGER,
                UserID INTEGER REFERENCES ev.OcmUser(ID),
                Username VARCHAR(200)
            );
        --END
        --$do$
        """
        # execute the query
        try:
            cur.execute(strSql)
        except Exception as e: 
            print(e)
                
        cur.close()
        conn.commit()
        conn.close()

    def InsertChargers(self, chargers):
        conn = self.Connect()

        for charger in chargers:
            query = """
                INSERT INTO ev.AddressInfo 
                (
                    AccessComments,
                    AddressLine1,
                    AddressLine2,
                    ContactEmail,
                    ContactTelephone1,
                    ContactTelephone2,
                    CountryID,
                    DistanceUnit,
                    ID,
                    Latitude,
                    Longitude,
                    Postcode,
                    RelatedURL,
                    StateOrProvince,
                    Title,
                    Town
                ) 
                SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (SELECT 1 FROM ev.AddressInfo WHERE ID = %s);
            """
            try:
                # create a cursor object called cur
                cur = conn.cursor()
                cur.execute(query, (charger.AddressInfo.AccessComments, charger.AddressInfo.AddressLine1,charger.AddressInfo.AddressLine2,
                            charger.AddressInfo.ContactEmail,charger.AddressInfo.ContactTelephone1,charger.AddressInfo.ContactTelephone2,
                            charger.AddressInfo.CountryID,charger.AddressInfo.DistanceUnit,charger.AddressInfo.ID,charger.AddressInfo.Latitude,
                            charger.AddressInfo.Longitude,charger.AddressInfo.Postcode,charger.AddressInfo.RelatedURL,charger.AddressInfo.StateOrProvince,
                            charger.AddressInfo.Title,charger.AddressInfo.Town, charger.AddressInfo.ID))
            except Exception as e:
                print('Address Exception: ', e)
            cur.close()
            conn.commit()

            query = """
                UPDATE ev.AddressInfo SET Location=st_SetSrid(st_MakePoint(Longitude, Latitude), 4326) WHERE ID = {0};
            """.format(charger.AddressInfo.ID)
            try:
                cur = conn.cursor()
                cur.execute(sql.SQL(query))
            except Exception as e:
                print('Update address info error: ', e)
            cur.close()
            conn.commit()

            chargerInsertQuery = """
                INSERT INTO ev.Charger
                (
                    ID,
                    AddressInfoID,
                    DataProviderID,
                    DataQualityLevel,
                    DateCreated,
                    DateLastStatusUpdate,
                    DateLastVerified,
                    GeneralComments,
                    IsRecentlyVerified,
                    NumberOfPoints,
                    OperatorID,
                    StatusTypeID,
                    SubmissionStatusTypeID,
                    UUID,
                    UsageCost,
                    UsageTypeID
                )
                SELECT %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                WHERE NOT EXISTS (SELECT 1 FROM ev.Charger WHERE ID = %s);
            """
            try:
                cur = conn.cursor()
                cur.execute(chargerInsertQuery, (charger.ID, charger.AddressInfo.ID, charger.DataProviderID,
                                                charger.DataQualityLevel, charger.DateCreated, charger.DateLastStatusUpdate,
                                                charger.DateLastVerified, charger.GeneralComments, charger.IsRecentlyVerified,
                                                charger.NumberOfPoints, charger.OperatorID, charger.StatusTypeID, charger.SubmissionStatusTypeID, 
                                                charger.UUID, charger.UsageCost,charger.UsageTypeID, charger.ID))
            except Exception as e:
                print("Charger exception: ", e)
                print(charger.DateCreated, ' ', charger.DateLastStatusUpdate, ' ', charger.DateLastVerified, ' ', charger.UsageCost)

            cur.close()
            conn.commit()
            
            for c in charger.Connections:
                connectionInsertQuery ="""
                INSERT INTO ev.Connection 
                (
                    ID,
                    ChargerID,
                    Amps,
                    ConnectionTypeID,
                    CurrentTypeID,
                    LevelID,
                    PowerKw,
                    Quantity,
                    StatusTypeID,
                    Voltage
                ) 
                SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (SELECT 1 FROM ev.Connection WHERE ID = %s);
                """
                try:
                    cur = conn.cursor()
                    cur.execute(connectionInsertQuery, (c.ID, charger.ID, c.Amps, c.ConnectionTypeID, c.CurrentTypeID, c.LevelID, c.PowerKw, c.Quantity,
                                c.StatusTypeID, c.Voltage, c.ID))
                except Exception as e:
                    print('Connection insert exception: ', e)

                cur.close()
                conn.commit()

            for mi in charger.MediaItems:
                if mi.User != None:
                    mediaUserInsertQuery = """
                        DO
                        $do$
                        BEGIN
                            CREATE EXTENSION IF NOT EXISTS dblink; -- enable extension 
                            IF NOT EXISTS(SELECT (NULL) FROM ev.OcmUser WHERE ID = {0})
                            THEN
                                INSERT INTO ev.OcmUser
                                (
                                    ID,
                                    ProfileImageURL,
                                    ReputationPoints,
                                    Username
                                )
                                VALUES(%s, %s, %s, %s);
                            END IF;
                        END
                        $do$
                            """.format(mi.User.ID)
                    try:
                        cur = conn.cursor()
                        cur.execute(mediaUserInsertQuery, (mi.User.ID, mi.User.ProfileImageURL, mi.User.ReputationPoints, mi.User.Username))
                    except Exception as e:
                        print('media item user insert exception: ', e)

                    cur.close()
                    conn.commit()

                mediaInsertQuery = """
                        INSERT INTO ev.MediaItem
                        (
                            ID,
                            ChargePointID,
                            Comment,
                            DateCreated,
                            IsEnabled,
                            IsExternalResource,
                            IsFeaturedItem,
                            IsVideo,
                            ItemThumbnailURL,
                            ItemURL,
                            UserID
                        )
                        SELECT %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s 
                        WHERE NOT EXISTS (SELECT 1 FROM ev.MediaItem WHERE Id = %s);

                    """

                try:
                    cur = conn.cursor()
                    params = (mi.ID,mi.ChargePointID, mi.Comment, mi.DateCreated,
                                        mi.IsEnabled, mi.IsExternalResource, mi.IsFeaturedItem,
                                        mi.IsVideo, mi.ItemThumbnailURL, mi.ItemURL,
                                        mi.User.ID, mi.ID)
                    cur.execute(mediaInsertQuery , params)
                except Exception as e:
                    print('Media item insert exception: ', e)
                    print('User: ', mi.User.ID, mi.User.ProfileImageURL, mi.User.ReputationPoints, mi.User.Username)
                    print('MI: ', mi.ID,mi.ChargePointID, mi.Comment, mi.DateCreated,
                                        mi.IsEnabled, mi.IsExternalResource, mi.IsFeaturedItem,
                                        mi.IsVideo, mi.ItemThumbnailURL, mi.ItemURL,
                                        mi.User.ID)

                cur.close()
                conn.commit()

            for uc in charger.UserComments:
                if uc.User != None:
                    try:
                        userCommentUserInsertQuery = """
                        DO
                        $do$
                        BEGIN
                            IF NOT EXISTS(SELECT (NULL) FROM ev.OcmUser WHERE ID = {0})
                            THEN
                                INSERT INTO ev.OcmUser
                                (
                                    ID,
                                    ProfileImageURL,
                                    ReputationPoints,
                                    Username
                                )
                                Values(%s, %s, %s, %s);
                            END IF;
                        END
                        $do$
                            """.format(uc.User.ID)

                        cur = conn.cursor()
                        cur.execute(userCommentUserInsertQuery, (uc.User.ID, uc.User.ProfileImageURL, uc.User.ReputationPoints, uc.User.Username))
                    except Exception as e:
                        print('usercomment user insert exception: ',e)
                        print(uc.User)
                        print(uc)
                    cur.close()
                    conn.commit()
                    
                userCommentInsertQuery = """
                        INSERT INTO ev.UserComment
                        (
                            ID,
                            ChargePointID,
                            CheckinStatusTypeID,
                            CommentTypeID,
                            DateCreated,
                            Rating,
                            UserID,
                            Username
                        )
                        SELECT %s,%s,%s,%s, %s,%s,%s,%s
                        WHERE NOT EXISTS (SELECT 1 FROM ev.UserComment WHERE ID = %s);
                    """

                try:
                    cur = conn.cursor()
                    params = (
                        uc.ID, 
                        uc.ChargePointID, 
                        uc.CheckinStatusTypeID,
                        uc.CommentTypeID, 
                        uc.DateCreated, 
                        uc.Rating,
                        uc.User.ID if uc.User != None else None,
                        uc.UserName,
                        uc.ID)
                    
                    cur.execute(userCommentInsertQuery, params)
                except Exception as e:
                    print('Usercomment insert exception: ',e)

                cur.close()
                conn.commit()
        conn.close()

    def dropDatabase(self):
        conn = self.Connect()
        # create a cursor object called cur
        cur = conn.cursor()
                
        # construct a query string
        strSql = """
        DROP TABLE ev.usercomment;
        DROP TABLE ev.mediaitem;
        DROP TABLE ev.OcmUser;
        DROP TABLE ev.connection;
        DROP TABLE ev.charger;
        DROP TABLE ev.addressinfo;
        """
        cur.execute(strSql)
        cur.close()
        conn.commit()
        conn.close()

    def GetNearestChargersFromDatabase(self, route, distance):

        linestring = ""

        for point in route[:-1]:
            linestring += str(point[1]) + ' ' + str(point[0]) + ','

        linestring += str(route[-1][1]) + ' ' + str(route[-1][0])

        nearest_point_query = """
            WITH line AS (SELECT ST_GeomFromText('LINESTRING({0})', 4326) AS geom)
                
            SELECT
                c.ID AS ID,
                c.UsageCost AS UsageCost,
                ai.ID AS AddressInfoID, 
                ai.AccessComments AS AccessComments,
                ai.AddressLine1 AS AddressLine1,
                ai.AddressLine2 AS AddressLine2,
                ai.Latitude AS Latitude,
                ai.Longitude AS Longitude,
                ai.Title AS Title,
				con.ID AS ConnectionID,
                con.Amps AS Amps,
                con.PowerKw AS PowerKw,
                con.Voltage AS Voltage,
                ST_Y(ST_ClosestPoint((SELECT geom FROM line), ST_MakePoint(ai.longitude, ai.latitude)::geography::geometry)) AS intersectionlatitude,
                ST_X(ST_ClosestPoint((SELECT geom FROM line), ST_MakePoint(ai.longitude, ai.latitude)::geography::geometry)) AS intersectionlongitude,
                ST_Distance(ST_MakePoint(ai.longitude, ai.latitude)::geography, (SELECT geom FROM line)) AS DistanceFromRoute
            FROM
                ev.charger c
                JOIN ev.addressinfo ai on c.addressinfoid = ai.id
				JOIN ev.connection con on c.id = con.chargerid
																				 
            WHERE 
				con.levelid = 3
                AND ST_DWithin(ST_MakePoint(ai.longitude, ai.latitude)::geography, (SELECT geom FROM line), {1})
            ORDER BY
                ai.Latitude DESC,
                ai.Longitude DESC;
        """.format(linestring, distance * 1609.344)

        try:
            conn = self.Connect()
            # create a cursor object called cur
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(nearest_point_query)
            chargerData = cur.fetchall()
        except Exception as e:
            raise e
        finally:
            conn.commit()
            cur.close()
            conn.close()
            
        if chargerData:
            return self.GetChargerObjects(chargerData)
        else:
            return []

    def GetChargerObjects(self, chargerData):
        chargers = []
        for charger in chargerData:
            isInCharger, index = self.IsInChargers(charger['id'], chargers)
            if isInCharger:
                chargers[index].Connections.append(Connection(amps=charger['amps'], ID=charger['connectionid'], powerKw=charger['powerkw'], voltage=charger['voltage']))
            else:
                chargers.append(Charger(addressInfo=AddressInfo(addressLine1=charger['addressline1'], addressLine2=charger['addressline2'], ID=charger['addressinfoid'], lat=charger['latitude'],long=charger['longitude'], title=charger['title']), connections=[Connection(amps=charger['amps'], ID=charger['connectionid'], powerKw=charger['powerkw'], voltage=charger['voltage'])], ID=charger['id'], usageCost=int(charger['usagecost']) if self.CanParseInt(charger['usagecost']) else 0.13, intersectionLatitude=charger['intersectionlatitude'], intersectionLongitude=charger['intersectionlongitude']))

        return chargers

    def IsInChargers(self, id, chargers):
        for charger in chargers:
            if charger.ID == id:
                return True, chargers.index(charger) 
        return False, -1

    def CanParseInt(self, value):
        try:
            integer = int(value)
            return True
        except:
            return False