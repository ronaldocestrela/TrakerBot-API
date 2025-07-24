using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance.Configurations;

public class UtmConfiguration : IEntityTypeConfiguration<Utm>
{
    public void Configure(EntityTypeBuilder<Utm> builder)
    {
        // Primary Key
        builder.HasKey(u => u.Id);

        // Properties configuration
        builder.Property(u => u.Name)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(u => u.Value)
            .IsRequired()
            .HasMaxLength(500);

        builder.Property(u => u.Source)
            .HasMaxLength(100);

        builder.Property(u => u.Medium)
            .HasMaxLength(100);

        builder.Property(u => u.Campaign)
            .HasMaxLength(200);

        builder.Property(u => u.UserId)
            .IsRequired(false);

        // Relationships
        // Many-to-one with ApplicationUser
        builder.HasOne(u => u.User)
            .WithMany()
            .HasForeignKey(u => u.UserId)
            .OnDelete(DeleteBehavior.SetNull);

        // Many-to-many with GeneratedLink is configured in GeneratedLinkConfiguration

        // Table configuration
        builder.ToTable("Utms");

        // Indexes
        builder.HasIndex(u => u.Name);
        builder.HasIndex(u => u.Source);
        builder.HasIndex(u => u.Medium);
        builder.HasIndex(u => u.Campaign);
        builder.HasIndex(u => u.UserId);

        // Composite index for common UTM parameter queries
        builder.HasIndex(u => new { u.Source, u.Medium, u.Campaign })
            .HasDatabaseName("IX_Utms_Source_Medium_Campaign");
    }
}
