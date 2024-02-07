import settings
import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv
load_dotenv()


def run():
    intents = discord.Intents.all()
    intents.message_content = True

    
    bot = commands.Bot(command_prefix=";", intents=intents)
    
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

        from discord.ext import commands

    @bot.command()
    async def ping(ctx):
        await ctx.send(f"Pong! **{round(bot.latency * 1000)} ms**")

    @bot.command()
    async def promote(ctx, user: discord.Member):
    
    # Permission check remains the same
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.send("You don't have permission to use this command.")
        
        # Get perm_member and second_choice roles using IDs
        perm_member_role = ctx.guild.get_role(1160108367411433472)  # Replace with your perm_member_role_id
        second_choice_role = ctx.guild.get_role(1160148703189925899)  # Replace with your second_choice_role_id
        
        # Check if roles exist (error message added)
        if not perm_member_role or not second_choice_role:
            return await ctx.send("Invalid role IDs provided. Please contact an administrator.")
        
        # Check if user already has perm_member role
        if perm_member_role in user.roles:
            return await ctx.send(f"{user.mention} already is a Permanent member.")
        
        # Check if user has second_choice role (error message added)
        if second_choice_role not in user.roles:
            return await ctx.send(f"{user.mention} cannot be promoted")
        
        # Remove second_choice role and add perm_member role
        await user.remove_roles(second_choice_role)
        await user.add_roles(perm_member_role)
        await ctx.send(f"{user.mention} has been promoted to a **Permanent member**!")

        @bot.command()
        async def demote(ctx, user: discord.Member):

        # Same permission check and role retrieval
            if not ctx.author.guild_permissions.manage_roles:
                return await ctx.send("You don't have permission to use this command.")
            perm_member_role = ctx.guild.get_role(1160108367411433472)
            second_choice_role = ctx.guild.get_role(1160148703189925899)
            if not perm_member_role or not second_choice_role:
                return await ctx.send("Invalid role IDs provided. Please contact an administrator.")

            # Check if user has neither role (error message added)
            if perm_member_role not in user.roles and second_choice_role not in user.roles:
                return await ctx.send(f"{user.mention} doesn't have either perm_member or 2nd_choice_member roles.")

            # Check if user has perm_member role
            if perm_member_role in user.roles:
                await user.remove_roles(perm_member_role)
                await user.add_roles(second_choice_role)
                await ctx.send(f"{user.mention} has been demoted to **2nd Choice Member**.")
            else:
                await ctx.send(f"{user.mention} doesn't have the perm_member role to be demoted.")

        @bot.command()
        async def shutdown(ctx):
        
        # Check if user has permission
            if not ctx.author.guild_permissions.manage_bot:
                return await ctx.send("You don't have permission to use this command.")
            
            # Send confirmation message
            await ctx.send("Shutting down...")
            
            # Disconnect from Discord
            await bot.logout()

        @bot.command()
        async def restart(ctx):
        
            # Check if user has permission
            if not ctx.author.guild_permissions.manage_bot:
                return await ctx.send("You don't have permission to use this command.")
            
            def restart_bot(): 
                os.execv(sys.executable, ['python'] + sys.argv)

            @bot.command(name= 'restart')
            async def restart(ctx):
                await ctx.send("Restarting bot...")
                restart_bot()

        




    
    bot.run(os.getenv("DISCORD_API_TOKEN"))


if __name__ == "__main__":
    run() 