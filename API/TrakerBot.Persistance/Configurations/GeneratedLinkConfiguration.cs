using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance.Configurations;

public class GeneratedLinkConfiguration : IEntityTypeConfiguration<GeneratedLink>
{
    public void Configure(EntityTypeBuilder<GeneratedLink> builder)
    {
        // Primary Key
        builder.HasKey(gl => gl.Id);

        // Properties configuration
        builder.Property(gl => gl.NewLink)
            .IsRequired()
            .HasMaxLength(2048);

        builder.Property(gl => gl.ShortLink)
            .IsRequired()
            .HasMaxLength(255);

        builder.Property(gl => gl.Clicks)
            .IsRequired()
            .HasMaxLength(50);

        builder.Property(gl => gl.OriginalLinkId)
            .IsRequired();

        builder.Property(gl => gl.UserId)
            .IsRequired();

        // Relationships
        // One-to-many with OriginalLink
        builder.HasOne(gl => gl.OriginalLink)
            .WithMany()
            .HasForeignKey(gl => gl.OriginalLinkId)
            .OnDelete(DeleteBehavior.Cascade);

        // One-to-many with ApplicationUser
        builder.HasOne(gl => gl.User)
            .WithMany()
            .HasForeignKey(gl => gl.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        // Many-to-many with Utm
        builder.HasMany(gl => gl.Utms)
            .WithMany(u => u.GeneratedLinks)
            .UsingEntity<Dictionary<string, object>>(
                "GeneratedLinkUtm",
                j => j.HasOne<Utm>().WithMany().HasForeignKey("UtmId"),
                j => j.HasOne<GeneratedLink>().WithMany().HasForeignKey("GeneratedLinkId"),
                j =>
                {
                    j.HasKey("GeneratedLinkId", "UtmId");
                    j.ToTable("GeneratedLinkUtms");
                });

        // Table configuration
        builder.ToTable("GeneratedLinks");

        // Indexes
        builder.HasIndex(gl => gl.ShortLink)
            .IsUnique();

        builder.HasIndex(gl => gl.OriginalLinkId);
        builder.HasIndex(gl => gl.UserId);
    }
}
