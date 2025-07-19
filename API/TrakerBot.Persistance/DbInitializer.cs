using Microsoft.AspNetCore.Identity;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance;

public class DbInitializer
{
    public static async Task SeedData(ApplicationDbContext context, UserManager<ApplicationUser> userManager, RoleManager<ApplicationRole> roleManager)
    {
        // Roles initialize
        var roles = new List<ApplicationRole>
        {
            new() { Name = "Admin" },
            new() { Name = "User" },
            new() { Name = "Expert" }
        };
        if (!context.Roles.Any())
        {
            foreach (var role in roles)
            {
                await roleManager.CreateAsync(role);
            }
        }

        // Users initialize
        var appUser = new List<ApplicationUser>
        {
            new() {
                FirstName = "Admin",
                LastName = "Admin",
                UserName = "admin@admin.com",
                Email = "admin@admin.com",
                EmailConfirmed = true,
                PhoneNumberConfirmed = true
            }
        };
        if (!userManager.Users.Any())
        {
            foreach (var user in appUser)
            {
                await userManager.CreateAsync(user, "Hadouken@69");
            }
        }

        // Assign roles to users
        var adminUser = await userManager.FindByEmailAsync("admin@admin.com");
        if (adminUser != null && !await userManager.IsInRoleAsync(adminUser, "Admin"))
        {
            await userManager.AddToRoleAsync(adminUser, "Admin");
        }

        await context.SaveChangesAsync();
    }
}
