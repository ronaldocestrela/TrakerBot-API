using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance.Configurations;

public class BookmakerConfiguration : IEntityTypeConfiguration<Bookmaker>
{
    public void Configure(EntityTypeBuilder<Bookmaker> builder)
    {
        // Primary Key
        builder.HasKey(b => b.Id);

        // Properties configuration
        builder.Property(b => b.Name)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(b => b.LogoUrl)
            .HasMaxLength(500);

        // Relationships
        // One-to-many with AffiliateCode
        builder.HasMany(b => b.AffiliateCodes)
            .WithOne(ac => ac.Bookmaker)
            .HasForeignKey(ac => ac.BookmakerId)
            .OnDelete(DeleteBehavior.Cascade);

        // Table configuration
        builder.ToTable("Bookmakers");

        // Indexes
        builder.HasIndex(b => b.Name)
            .IsUnique();
    }
}
