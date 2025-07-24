using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance.Configurations;

public class OriginalLinkConfiguration : IEntityTypeConfiguration<OriginalLink>
{
    public void Configure(EntityTypeBuilder<OriginalLink> builder)
    {
        // Primary Key
        builder.HasKey(ol => ol.Id);

        // Properties configuration
        builder.Property(ol => ol.Url)
            .IsRequired()
            .HasMaxLength(2048);

        builder.Property(ol => ol.UserId)
            .IsRequired(false);

        // Relationships
        // Many-to-one with ApplicationUser
        builder.HasOne(ol => ol.User)
            .WithMany()
            .HasForeignKey(ol => ol.UserId)
            .OnDelete(DeleteBehavior.SetNull);

        // Table configuration
        builder.ToTable("OriginalLinks");

        // Indexes
        builder.HasIndex(ol => ol.Url);
        builder.HasIndex(ol => ol.UserId);
    }
}
