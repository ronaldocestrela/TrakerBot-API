using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance.Configurations;

public class AffiliateCodeConfiguration : IEntityTypeConfiguration<AffiliateCode>
{
    public void Configure(EntityTypeBuilder<AffiliateCode> builder)
    {
        // Primary Key
        builder.HasKey(ac => ac.Id);

        // Properties configuration
        builder.Property(ac => ac.Code)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(ac => ac.UserId)
            .IsRequired(false);

        builder.Property(ac => ac.BookmakerId)
            .IsRequired(false);

        // Relationships
        // Many-to-one with ApplicationUser
        builder.HasOne(ac => ac.User)
            .WithMany()
            .HasForeignKey(ac => ac.UserId)
            .OnDelete(DeleteBehavior.SetNull);

        // Many-to-one with Bookmaker
        builder.HasOne(ac => ac.Bookmaker)
            .WithMany(b => b.AffiliateCodes)
            .HasForeignKey(ac => ac.BookmakerId)
            .OnDelete(DeleteBehavior.Cascade);

        // Table configuration
        builder.ToTable("AffiliateCodes");

        // Indexes
        builder.HasIndex(ac => ac.Code);
        builder.HasIndex(ac => ac.UserId);
        builder.HasIndex(ac => ac.BookmakerId);

        // Composite index for user-bookmaker combination
        builder.HasIndex(ac => new { ac.UserId, ac.BookmakerId })
            .HasDatabaseName("IX_AffiliateCodes_User_Bookmaker");
    }
}
