using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance.Configurations;

public class ApplicationRoleConfiguration : IEntityTypeConfiguration<ApplicationRole>
{
    public void Configure(EntityTypeBuilder<ApplicationRole> builder)
    {
        // Properties configuration
        builder.Property(r => r.Name)
            .IsRequired()
            .HasMaxLength(256);

        builder.Property(r => r.NormalizedName)
            .HasMaxLength(256);

        // Indexes
        builder.HasIndex(r => r.NormalizedName)
            .IsUnique()
            .HasDatabaseName("RoleNameIndex");

        // Table configuration
        builder.ToTable("AspNetRoles");
    }
}
