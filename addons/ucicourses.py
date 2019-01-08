import discord
import utilities.catalogue
from discord.ext import commands


class UCICourses:
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def coursealias(self, ctx):
        '''creates an alias - [alias] : [department]
        aliases must be one word'''
        if not re.match("^.* : .*$", ctx.message.content):
            await ctx.send("**" + ctx.message.content + "**\n Incorrect format, please use -> [alias] : [department]")
        else:
            message = ctx.message.content.split()
            message = " ".join(message[1:len(message)])
            message = message.split(" : ")
            # print(message)
            self.bot.guild_data["cataloguealiases"][message[0].lower()] = message[1].lower()
            self.bot.dump()

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def removealias(self, ctx, alias):
        '''removes an alias - [alias]
        aliases must be one word'''
        del self.bot.guild_data["cataloguealiases"][alias.lower()]
        await ctx.send(alias.lower(), "deleted")

    # @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def getaliases(self, ctx):
        '''gets all aliases'''
        embeded = discord.Embed(title="Course Aliases")
        for key, value in self.bot.guild_data["cataloguealiases"].items():
            embeded.add_field(name="Alias = " + key, value="Original = " + value, inline=False)
        await ctx.send(embed=embeded)

    @commands.guild_only()
    @commands.command()
    async def courseinfo(self, ctx):
        '''gets info for a course'''
        try:
            course_to_find = ctx.message.content.split()
            course_to_find = " ".join(course_to_find[1:len(course_to_find)])
            try:
                split = course_to_find.split()
                tag = " ".join(split[len(split) - 1:])
                alias = " ".join(split[0:len(split) - 1])
                real_course = self.bot.guild_data["cataloguealiases"][alias]
                course_to_find = real_course + " " + tag
                course = utilities.catalogue.get_course(course_to_find)
            except KeyError:
                course = utilities.catalogue.get_course(course_to_find)
            try:
                nembed = discord.Embed(title="**" + course.course_title + "**",
                                       description="**" + course.courseID + "**" + " - " + "*" +
                                                   course.course_units + "*",
                                       color=1938213)
                nembed.add_field(name="Course Description", value=course.course_desc, inline=False)
                if course.prereqs is not None:
                    nembed.add_field(name="Requisites", value=course.prereqs, inline=False)
                if course.restrictions is not None:
                    nembed.add_field(name="Restrictions", value=course.restrictions.rstrip("Restriction:"),
                                     inline=False)
                if course.overlaps is not None:
                    nembed.add_field(name="Course Overlaps", value=course.overlaps, inline=False)
                if course.concurrent is not None:
                    nembed.add_field(name="Course Concurrent", value=course.concurrent, inline=False)
                if course.same_as is not None:
                    nembed.add_field(name="Same Course", value=course.same_as, inline=False)
                if course.grading_option is not None:
                    nembed.add_field(name="Grading Options", value=course.grading_option.rstrip("Grading Option:"),
                                     inline=False)
                if course.repeatability is not None:
                    nembed.add_field(name="Repeatability", value=course.repeatability.rstrip("Repeatability:"),
                                     inline=False)
                if course.spillover != list():
                    nembed.add_field(name="Not Implemented", value=course.spillover, inline=False)
                await ctx.send(embed=nembed)
            except AttributeError:
                await ctx.send("{ucicourse} was unable to be found\n"
                               "Make sure you are course section identifier. It should be "
                               "the same format as the UCI Course Catalogue.\n"
                               "Examples: MATH, PHY SCI, I&C SCI, CRM/LAW, EARTHSS, BIO SCI".format(
                                ucicourse=course_to_find))
        except Exception as e:
            ctx.send("I dont know what happened but something broke, ping Lamp so he can figure it out and fix it")
            print("ERROR: " + e)

    @commands.guild_only()
    @commands.command()
    async def getcoursetags(self, ctx, letter):
        '''gets course tags for a specific starting letter'''
        try:
            course_ids = utilities.catalogue.get_course_ids(letter.upper())
            ids = "\n".join(course_ids)
            embedded = discord.Embed(title="**Course Tags for - " + letter.upper() + "**",
                                     description=ids,
                                     color=1938213)
            # for id in course_ids:
            #     embedded.add_field(name=id, value="\u200b", inline=False)
            await ctx.send(embed=embedded)

        except AttributeError as a:
            embedded = discord.Embed(title="**NO TAGS FOUND FOR - " + letter.upper() + "**")
            await ctx.send(embed=embedded)
        except Exception as e:
            print(e.__name__)


def setup(bot):
    bot.add_cog(UCICourses(bot))
