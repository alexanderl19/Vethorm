import asyncio
import asyncpg
import unittest
from bot import Vethorm
import utilities.vqueries as vquery

from pathlib import Path
import sys

parent = Path('/home/kyle/personal/project-repos/Vethorm/')
sys.path.insert(0, parent)

class TestVqueryMethods(unittest.TestCase):
    def setUp(self):
        self.bot = Vethorm()
        self.run = asyncio.get_event_loop().run_until_complete
    
    def test_guild(self):
        self.run( vquery.insert_guild(self.bot, 1) ) 
        results = self.run( vquery.request_guilds(self.bot) )

        assert results == {1 : {'watch_mode' : False}}
        assert self.bot.Vguilds == {1 : {'watch_mode' : False}}

        self.run( vquery.remove_guild(self.bot, 1) )
        results = self.run( vquery.request_guilds(self.bot) )

        assert results == {}
        assert self.bot.Vguilds == {}

    def test_user(self):
        try:
            self.run( vquery.insert_user(self.bot, 10, 1) )
        except asyncpg.exceptions.ForeignKeyViolationError:
            pass

        self.run( vquery.insert_guild(self.bot, 1) )
        self.run( vquery.insert_user(self.bot, 10, 1) )

        results = self.run( vquery.request_users(self.bot) )
        
        try:
            assert results == {1 : {10} }
            assert self.bot.Vusers ==  {1 : {10} }
        except Exception as e:
            print('==== Error check 1 ====')
            print(results)
            print(self.bot.Vusers)
            raise e

        self.run( vquery.remove_user(self.bot, 10, 1) )
        self.run( vquery.remove_guild(self.bot, 1) )
        assert self.bot.Vguilds == {}
        results = self.run( vquery.request_users(self.bot) )
        try:
            assert results == {}
            assert self.bot.Vusers ==  {1 : set() }
        except Exception as e:
            print('==== Error check 2 ====')
            print(results)
            print(self.bot.Vusers)
            raise e

    def test_catalogue(self):
        self.run( vquery.insert_guild(self.bot, 1) )

        self.run( vquery.insert_catalogue_alias(self.bot, 'I&C SCI', 'ics', 1) )

        results = self.run( vquery.request_catalogue_aliases(self.bot) )

        try:
            assert results == {1 : {'ics' : 'I&C SCI'} }
            assert self.bot.Valiases == {1 : {'ics' : 'I&C SCI'}}
        except Exception as e:
            print('==== Error check 1 ====')
            print(results)
            print(self.bot.Valiases)
            raise e
        finally:
            self.run( vquery.remove_catalogue_alias(self.bot, 'ics', 1) )
            self.run( vquery.remove_guild(self.bot, 1) )

            results = self.run( vquery.request_catalogue_aliases(self.bot) )
            try:
                assert results == {}
                assert self.bot.Valiases == {1 : {}}
            except Exception as e:
                print('==== Error check 2 ====')
                print(results)
                print(self.bot.Valiases)
                raise e

    def test_tag(self):
        self.run( vquery.insert_guild(self.bot, 1) )
        self.run( vquery.insert_tag(self.bot, 'ics', 1, 'information and comp sci') )

        results = self.run( vquery.request_tags(self.bot) )

        try:
            results == {1 : {'ics' : 'information and comp sci'}}
            self.bot.Vtags == {1 : {'ics' : 'information and comp sci'}}
        except Exception as e:
            print('==== Error check 1 ====')
            raise e
        finally:
            self.run( vquery.remove_tag(self.bot, 'ics', 1) )
            self.run( vquery.remove_guild(self.bot, 1) )
        
        results = self.run( vquery.request_tags(self.bot) )  
        try:
            results == {}
            self.bot.Vtags == {1 : {}}
        except Exception as e:
            print('==== Error check 2 ====')
            raise e

    def test_channel(self):
        pass
        # TODO: fix channel functions and finish unit tests

        self.run( vquery.insert_guild(self.bot, 1) )
        self.run( vquery.insert_channel(self.bot, 100, 1) )

        results = self.run( vquery.request_channels(self.bot) )
        try:
            assert results == {1 : {100} }
            assert self.bot.Vchans == {1 : {100} }
        except Exception as e:
            print('==== Error check 1 ====')
            raise e
        finally:
            self.run( vquery.remove_channel(self.bot, 100, 1) )
            self.run( vquery.remove_guild(self.bot, 1) )

        results = self.run( vquery.request_channels(self.bot) )
        try:
            assert results == {}
            assert self.bot.Vchans == {1 : set() }
        except Exception as e:
            print('==== Error check 2 ====')
            raise e
        



        


        

if __name__ == '__main__':
    unittest.main()