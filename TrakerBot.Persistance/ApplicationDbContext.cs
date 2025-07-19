using System.Reflection;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance;

public class ApplicationDbContext(DbContextOptions options) : IdentityDbContext<ApplicationUser, ApplicationRole, string>(options)
{
    public DbSet<Bookmaker> Bookmakers { get; set; }
    public DbSet<OriginalLink> OriginalLinks { get; set; }
    public DbSet<Utm> Utms { get; set; }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        builder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }
}
